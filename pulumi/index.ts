import * as docker from '@pulumi/docker';
import * as gcp from '@pulumi/gcp';
import * as pulumi from '@pulumi/pulumi';
import * as command from '@pulumi/command';

import { join } from 'path';

const rootPath = join(__dirname, '..');

const commitHash = new command.local.Command('commit-hash', {
  create: 'git rev-parse --short HEAD',
});

const activateArtifactRepository = new gcp.projects.Service(
  'artifact-repository',
  {
    disableDependentServices: true,
    service: 'artifactregistry.googleapis.com',
  }
);

const artifactRepository = new gcp.artifactregistry.Repository(
  'pathway',
  {
    description: 'Docker repository',
    format: 'DOCKER',
    location: 'europe-west1',
    repositoryId: 'pathway',
  },
  {
    dependsOn: [activateArtifactRepository],
  }
);

const pathwayServiceName = 'pathway-service';
const pathwayServiceImage = new docker.Image(pathwayServiceName, {
  imageName: pulumi.interpolate`europe-west1-docker.pkg.dev/${gcp.config.project}/${artifactRepository.name}/pathway-service:${commitHash.stdout}`,
  build: {
    context: rootPath,
    dockerfile: join(rootPath, 'src/pathway_service/Dockerfile'),
  },
});

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
            image: pathwayServiceImage.imageName,
            // @todo try this
            // resources: {
            //   limits: {
            //     memory: '4g',
            //   },
            // },
          },
        ],
      },
    },
    traffics: [
      {
        percent: 100,
        latestRevision: true,
        tag: pulumi.interpolate`commit-${commitHash.stdout}`,
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
