import uuid
from typing import Dict

from domain.models import Cluster
from services.communication import execute_ssh_raspberry_command
from settings import Settings
from src.services import Handler


class GetAllClustersHandler(Handler):

    def handle(self):
        with self.manager.start() as uow:
            clusters = uow.clusters.get_all()
            clusters_list = [cluster.as_dict() for cluster in clusters]

        return clusters_list


class AddClusterHandler(Handler):

    def handle(self, body: dict):
        body["cluster_id"] = uuid.uuid4()
        with self.manager.start() as uow:
            uow.clusters.add_cluster(Cluster(**body))


class GetSingleClusterHandler(Handler):
    def handle(self, id=None, cluster_name=None):
        with self.manager.start() as uow:
            if id:
                cluster = uow.clusters.get_by_id(id)
            elif cluster_name:
                cluster = uow.clusters.get_by_name(cluster_name)

        return cluster.as_dict()


class AddRaspberryPiToClusterHandler(Handler):
    def handle(self, id, mac_address: Dict):
        with self.manager.start() as uow:
            cluster_to_update = uow.clusters.get_by_id(id)
            raspberry_to_add = uow.raspberry_pis.get_by_mac_address(mac_address)
            cluster_to_update.raspberry_pis.append(raspberry_to_add)
            execute_ssh_raspberry_command(command=f"k3s agent "
                                                  f"--token value={Settings.server_token} "
                                                  f"--node-name={raspberry_to_add.name} "
                                                  f"--server value={Settings.server_address}:6443 "
                                                  f"--snapshotter=native",
                                          address=raspberry_to_add.address)

