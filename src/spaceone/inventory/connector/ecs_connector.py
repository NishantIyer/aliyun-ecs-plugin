__all__ = ["ECSConnector"]

import json
import logging

from aliyunsdkcore import client
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeDisksRequest import DescribeDisksRequest
from aliyunsdkecs.request.v20140526.DescribeImagesRequest import DescribeImagesRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import (
    DescribeInstancesRequest,
)
from aliyunsdkecs.request.v20140526.DescribeNetworkInterfacesRequest import (
    DescribeNetworkInterfacesRequest,
)
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupAttributeRequest import (
    DescribeSecurityGroupAttributeRequest,
)
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupsRequest import (
    DescribeSecurityGroupsRequest,
)
from aliyunsdkess.request.v20140828.DescribeScalingGroupsRequest import (
    DescribeScalingGroupsRequest,
)
from aliyunsdkess.request.v20140828.DescribeScalingInstancesRequest import (
    DescribeScalingInstancesRequest,
)
from aliyunsdkslb.request.v20140515.DescribeLoadBalancerAttributeRequest import (
    DescribeLoadBalancerAttributeRequest,
)
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import (
    DescribeLoadBalancersRequest,
)
from aliyunsdkvpc.request.v20160428.DescribeVSwitchesRequest import (
    DescribeVSwitchesRequest,
)
from aliyunsdkvpc.request.v20160428.DescribeVpcsRequest import DescribeVpcsRequest
from spaceone.core.connector import BaseConnector

_LOGGER = logging.getLogger(__name__)
RESOURCES = ["ecs"]

MAX_PAGE_NUM = 10
MAX_PAGE_SIZE = 50


class ECSConnector(BaseConnector):
    def __init__(self, transaction=None, config=None, **kwargs):
        super().__init__(transaction, config, **kwargs)
        self.ecs_client = None

    def verify(self, secret_data, region_name):
        self.set_client(secret_data, region_name)
        request = DescribeRegionsRequest()
        response = self._send_request(request)
        return "ACTIVE" if response is not None else "UNKNOWN"

    def set_client(self, secret_data, region_name):
        ali_access_key_id = secret_data["ali_access_key_id"].strip()
        ali_access_key_secret = secret_data["ali_access_key_secret"].strip()
        self.ecs_client = client.AcsClient(
            ali_access_key_id, ali_access_key_secret, region_name
        )

    def _send_request(self, request):
        # request._params["PageNumber"] = MAX_PAGE_NUM
        # request._params["PageSize"] = MAX_PAGE_SIZE
        request.set_accept_format("json")
        try:
            response_str = self.ecs_client.do_action_with_exception(request)
            response_detail = json.loads(response_str)
            return response_detail
        except ClientException as e:
            print(f"[Client Exception]: {e}")
        except ServerException as e:
            print(f"[Server Exception]: {e}")
        except Exception as e:
            print(f"[Error: fail to send {request}]: {e}")

    def list_regions(self, **params):
        regions = []
        request = DescribeRegionsRequest()
        request._params = params
        response = self._send_request(request)
        if response :
            regions.extend(response.get("Regions", []).get("Region", []))
        return regions

    def list_instances(self, **params):
        ecs_instances = []
        request = DescribeInstancesRequest()
        request._params = params
        response = self._send_request(request)
        if response :
            ecs_instances.extend(response.get("Instances", []).get("Instance", []))
        return ecs_instances

    def list_scaling_groups(self, **params):
        scaling_groups = []
        request = DescribeScalingGroupsRequest()
        request._params = params
        response = self._send_request(request)
        if response :
            scaling_groups.extend(
                response.get("ScalingGroups", {}).get("ScalingGroup", [])
            )
        return scaling_groups

    def list_scaling_instances(self, **params):
        scaling_instances = []
        request = DescribeScalingInstancesRequest()
        request._params = params
        response = self._send_request(request)
        if response :
            scaling_instances.extend(
                response.get("ScalingInstances", {}).get("ScalingInstance", [])
            )
        return scaling_instances

    def list_load_balancers(self, **params):
        load_balancers = []
        request = DescribeLoadBalancersRequest()
        request._params = params
        response = self._send_request(request)
        if response :
            load_balancers.extend(
                response.get("LoadBalancers", {}).get("LoadBalancer", [])
            )
        return load_balancers

    def list_load_balancer_attributes(self, load_balancer_id, **params):
        load_balancer_attributes = {}
        request = DescribeLoadBalancerAttributeRequest()
        request._params = params
        request.set_LoadBalancerId(load_balancer_id)
        response = self._send_request(request)
        if response :
            load_balancer_attributes.update(response)
        return load_balancer_attributes

    # def list_backend_servers(self, load_balancer_id, **params):
    #     backend_servers = []
    #     request = DescribeHealthStatusRequest()
    #     request.set_LoadBalancerId(load_balancer_id)
    #     request._params = params
    #     response = self._send_request(request)
    #     if response :
    #         backend_servers.extend(response.get("BackendServers", {}).get('BackendServer', []))
    #     return backend_servers

    def list_disks(self, **params):
        disks = []
        request = DescribeDisksRequest()
        request._params = params
        response = self._send_request(request)
        if response :
            disks.extend(response.get("Disks", {}).get("Disk", []))
        return disks

    # def list_images(self, **params):
    #     images = []
    #     request = DescribeImagesRequest()
    #     request._params = params
    #     response = self._send_request(request)
    #     if response :
    #         images.extend(response.get("Images", {}).get("Image", []))
    #     return images

    def list_vpcs(self, **params):
        vpcs = []
        request = DescribeVpcsRequest()
        request._params = params
        response = self._send_request(request)
        if response :
            vpcs.extend(response.get("Vpcs", {}).get("Vpc", []))
        return vpcs

    def list_subnets(self, **params):
        subnets = []
        request = DescribeVSwitchesRequest()
        request._params = params
        response = self._send_request(request)
        if response :
            subnets.extend(response.get("VSwitches", {}).get("VSwitch", []))
        return subnets

    def list_nics(self, **params):
        nics = []
        request = DescribeNetworkInterfacesRequest()
        request._params = params
        response = self._send_request(request)
        if response :
            nics.extend(
                response.get("NetworkInterfaceSets", {}).get("NetworkInterfaceSet", [])
            )
        return nics

    def list_security_groups(self, **params):
        sg_attributes = []
        request = DescribeSecurityGroupsRequest()
        request._params = params
        response = self._send_request(request)
        if response :
            sgs = response.get("SecurityGroups", {}).get("SecurityGroup", [])
            for sg in sgs:
                sg_attributes.append(
                    self.get_sg_attribute(sg.get("SecurityGroupId", None))
                )
        return sg_attributes

    def get_sg_attribute(self, sg_id):
        sg_attribute = {}
        request = DescribeSecurityGroupAttributeRequest()
        request.set_SecurityGroupId(sg_id)
        response = self._send_request(request)
        if response :
            sg_attribute.update(response)
        return sg_attribute
