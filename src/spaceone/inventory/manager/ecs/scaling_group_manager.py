
from spaceone.core.manager import BaseManager

from spaceone.inventory.model.scaling_group import ScalingGroup


class ScalingGroupManager(BaseManager):
    def __init__(self, params, ecs_connector=None):
        self.params = params
        self.ecs_connector = ecs_connector

    def get_scaling_info(self, instance_id, scaling_groups, scaling_instances):
        """
        data.scaling_group = {
            'id': '',
            'name': '',
            'active_scaling_configuration_id': '',
            'launch_template': {
                'id': '',
                'version': ''
            }
        }
        """
        if scaling_instances is None or scaling_groups is None:
            return None
        matched_scaling_group = self.get_matched_scaling_group(
            instance_id, scaling_groups, scaling_instances
        )

        if matched_scaling_group:
            scaling_group_data = {
                "id": matched_scaling_group.get("ScalingGroupId", ""),
                "name": matched_scaling_group.get("ScalingGroupName", ""),
            }

            if "LaunchTemplateId" in matched_scaling_group:
                scaling_group_data.update(
                    {
                        "launch_template": {
                            "id": matched_scaling_group.get("LaunchTemplateId", ""),
                            "version": matched_scaling_group.get(
                                "LaunchTemplateVersion", ""
                            ),
                        }
                    }
                )

            if "ActiveScalingConfigurationId" in matched_scaling_group:
                scaling_group_data.update(
                    {
                        "active_scaling_configuration_id": matched_scaling_group.get(
                            "ActiveScalingConfigurationId"
                        )
                    }
                )
            return ScalingGroup(scaling_group_data, strict=False)
        else:
            return None

    @staticmethod
    def get_matched_scaling_group(instance_id, scaling_groups, scaling_instances):
        matched_scaling_group_id = None
        for scaling_instance in scaling_instances:
            if instance_id == scaling_instance.get("InstanceId"):
                matched_scaling_group_id = scaling_instance.get("ScalingGroupId", "")

        for scaling_group in scaling_groups:
            if matched_scaling_group_id == scaling_group.get("ScalingGroupId", ""):
                return scaling_group
