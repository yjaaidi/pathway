import * as pulumi from '@pulumi/pulumi';
import * as gcp from '@pulumi/gcp';

const activateCloudRun = new gcp.projects.Service('cloud-run', {
  disableDependentServices: true,
  service: 'run.googleapis.com',
});

const pathwayService = new gcp.cloudrun.Service(
  'pathway-service',
  {
    location: 'europe-west1',
    template: {
      spec: {
        containers: [
          {
            image: 'gcr.io/cloudrun/hello',
          },
        ],
      },
    },
    traffics: [
      {
        percent: 100,
        latestRevision: true,
      },
    ],
  },
  {
    dependsOn: [activateCloudRun],
  }
);

const publicCloudRunPolicy = gcp.organizations.getIAMPolicy({
  bindings: [
    {
      role: 'roles/run.invoker',
      members: ['allUsers'],
    },
  ],
});

new gcp.cloudrun.IamPolicy('publicCloudRunPolicy', {
  location: pathwayService.location,
  service: pathwayService.name,
  policyData: publicCloudRunPolicy.then((policy) => policy.policyData),
});
