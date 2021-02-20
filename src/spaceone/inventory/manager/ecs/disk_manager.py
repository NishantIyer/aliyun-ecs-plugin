from spaceone.core.manager import BaseManager

from spaceone.inventory.model.disk import Disk


class DiskManager(BaseManager):
    def __init__(self, params, ecs_connector=None):
        self.params = params
        self.ecs_connector = ecs_connector

    def get_disk_info(self, instance_id, disks):
        """
        disk_data = {
            "device_index": 0,
            "device": "",
            "disk_type": "all" || "system" || "data",
            "size": 100,
            "tags": {
                "disk_id": "",
                "disk_name": "",
                "encrypted": true | false,
                "iops_read": 0,
                "iops_write": 0,
                "performance_level": "",
                "disk_charge_type": "PrePaid" || "PostPaid"
            }
        }
        """
        if disks is None:
            return None

        disks_data_list = []
        index = 0
        matched_disks = self.get_matched_disks(instance_id, disks)
        for matched_disk in matched_disks:
            disk_data = {
                "device": matched_disk.get("Device"),
                "device_index": index,
                "device_type": matched_disk.get("Type"),
                "size": matched_disk.get("Size"),
                "tags": {
                    "disk_id": matched_disk.get("DiskId"),
                    "disk_name": matched_disk.get("DiskName"),
                    "encrypted": matched_disk.get("Encrypted"),
                    "performance_level": matched_disk.get("PerformanceLevel"),
                    "disk_charge_type": matched_disk.get("DiskChargeType"),
                    "serial_number": matched_disk.get("SerialNumber", None),
                },
            }

            if "Iops" in matched_disk:
                disk_data["tags"].update(
                    {
                        "iops_read": matched_disk.get("IOPSRead"),
                        "iops_write": matched_disk.get("IOPSWrite"),
                    }
                )

            disks_data_list.append(Disk(disk_data, strict=False))
            index += 1

        return disks_data_list

    @staticmethod
    def get_matched_disks(instance_id, disks):
        matched_disks = []
        for disk in disks:
            if instance_id == disk.get("InstanceId"):
                matched_disks.append(disk)
        return matched_disks

    @staticmethod
    def get_volumes_from_ids(volume_ids, volumes):
        return [volume for volume in volumes if volume["VolumeId"] in volume_ids]

    @staticmethod
    def get_device(volume):
        attachments = volume.get("Attachments", [])

        for attachment in attachments:
            return attachment.get("Device")

        return ""
