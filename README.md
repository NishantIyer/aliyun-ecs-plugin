# plugin-alibaba-cloud-ecs
![Alibaba Cloud ECS](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/alibaba_cloud/logo.svg)
**Plugin for Alibaba Cloud ECS instances**

> My [plugin-alibaba-cloud-ecs](https://github.com/NishantIyer/plugin-alibaba-cloud-ecs) convenient tool to 
extract ECS instances data from Alibaba Cloud platform. 


Find this also at [Dockerhub](https://hub.docker.com/repository/docker/nishh2609/plugin-alibaba-cloud-plugin)
> Latest stable version : 1.0

Please contact me if you need any further information. (<nishant.iyer62@gmail.com>)

---

## Authentication Overview
Registered service account on SpaceONE must have certain permissions to collect cloud service data.<br/>
Please, set authentication privilege for followings:

#### [ECS](https://www.alibabacloud.com/help/doc-detail/25484.htm?spm=a2c63.p38356.b99.665.5fe944a8DuRPnT)

- ECS Instance
    - Scope(API operations by Packages)
        - aliyunsdkecs
            - [DescribeDisks](https://www.alibabacloud.com/help/doc-detail/25514.htm#t9885.html)
            - [DescribeInstances](https://www.alibabacloud.com/help/doc-detail/25506.htm#t9865.html)
            - [DescribeRegions](https://www.alibabacloud.com/help/doc-detail/25609.htm#t9972.html)
            - [DescribeSecurityGroupAttribute](https://www.alibabacloud.com/help/doc-detail/25555.htm#t9924.html)
            - [DescribeSecurityGroups](https://www.alibabacloud.com/help/doc-detail/25556.htm#t9925.html)
        - aliyunsdkess
            - [DescribeScalingGroups](https://www.alibabacloud.com/help/doc-detail/25938.htm#t40632.html)
            - [DescribeScalingInstances](https://www.alibabacloud.com/help/doc-detail/25942.htm#t40633.html)
        - aliyunsdkslb
            - [DescribeLoadBalancers](https://www.alibabacloud.com/help/doc-detail/27582.htm#t4187.html)
            - [DescribeLoadBalancerAttribute](https://www.alibabacloud.com/help/doc-detail/27583.htm#t4188.html)
        - aliyunsdkvpc           
            - [DescribeVSwitches](https://www.alibabacloud.com/help/doc-detail/35748.htm#t2482.html)
    - Permissions (Actions for Policies)
        - ecs.DescribeDisks
        - ecs.DescribeInstances
        - ecs.DescribeRegions
        - ecs.DescribeSecurityGroupAttribute
        - ecs.DescribeSecurityGroups
        - ess.DescribeScalingGroups
        - ess.DescribeScalingInstances
        - slb.DescribeLoadBalancers
        - slb.DescribeLoadBalancerAttribute
        - vpc.DescribeVSwitches

#Made by Nishant Iyer