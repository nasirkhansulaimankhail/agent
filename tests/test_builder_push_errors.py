import importlib.util
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from agent.builder import ImageBuilder, PatchImageBuilder
from agent.exceptions import AgentException

BUILDERS = [ImageBuilder, PatchImageBuilder]
if importlib.util.find_spec("agent.legacy_uploaded_builder"):
    from agent.legacy_uploaded_builder import ImageBuilder as LegacyImageBuilder
    BUILDERS.append(LegacyImageBuilder)


class TestBuilderPushErrors(unittest.TestCase):
    def run_stream(self, builder_type, events):
        builder = object.__new__(builder_type)
        builder.registry = {"url": "registry.invalid", "username": "lab", "password": "fixture"}
        builder.image_repository = "registry.invalid/fixture"
        builder.image_tag = "test"
        builder.output = {"push": []}
        builder._publish_throttled_output = Mock()
        client = SimpleNamespace(images=SimpleNamespace(push=Mock(return_value=iter(events))))
        if builder_type is PatchImageBuilder:
            with patch("agent.builder.docker.from_env", return_value=client):
                builder_type._push_patch_image.__wrapped__(builder)
        else:
            builder._push_image(client)
        return builder, client

    def test_decoded_error_event_fails_the_push(self):
        for builder_type in BUILDERS:
            with self.subTest(builder=builder_type.__module__):
                with self.assertRaises(AgentException) as caught:
                    self.run_stream(builder_type, [{"status": "Preparing"}, {"error": "registry unavailable"}])
                self.assertEqual(caught.exception.data["traceback"],
                                 "Docker image push failed: registry unavailable")

    def test_error_detail_without_top_level_error_fails_the_push(self):
        for builder_type in BUILDERS:
            with self.subTest(builder=builder_type.__module__):
                with self.assertRaises(AgentException) as caught:
                    self.run_stream(builder_type, [{"errorDetail": {"message": "permission denied"}}])
                self.assertEqual(caught.exception.data["traceback"],
                                 "Docker image push failed: permission denied")

    def test_unrecognized_nonempty_error_detail_fails_the_push(self):
        for builder_type in BUILDERS:
            with self.subTest(builder=builder_type.__module__):
                with self.assertRaises(AgentException) as caught:
                    self.run_stream(builder_type, [{"errorDetail": {"code": "UNKNOWN"}}])
                self.assertEqual(caught.exception.data["traceback"],
                                 "Docker image push failed: Unknown registry error")

    def test_successful_status_and_digest_events_are_preserved(self):
        events = [{"status": "Pushed"}, {"aux": {"Digest": "sha256:fixture"}}]
        for builder_type in BUILDERS:
            with self.subTest(builder=builder_type.__module__):
                builder, client = self.run_stream(builder_type, events)
                self.assertEqual(builder.output["push"], events)
                self.assertEqual(builder._publish_throttled_output.call_count,
                                 len(events) + 1)
                client.images.push.assert_called_once_with(
                    builder.image_repository, builder.image_tag, stream=True,
                    decode=True, auth_config={"username": "lab", "password": "fixture",
                                             "serveraddress": "registry.invalid"})
