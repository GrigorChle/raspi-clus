import os
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import create_engine


@dataclass
class Settings:

    db_engine = os.environ.get('DB_ENGINE') or "postgresql"
    db_user = os.environ.get('DB_USER') or "postgres"
    db_password = os.environ.get('DB_PASS') or "password"
    db_name = os.environ.get('DB_NAME') or "postgres"
    db_uri = os.environ.get('DB_URI') or "localhost"
    db_port = os.environ.get('DB_PORT') or 5432

    database_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_uri}:{db_port}/{db_name}"
    database_engine = create_engine(database_url, echo=True)

    server_token = os.environ.get("K3S_TOKEN")
    dhcp_configuration_file = Path(os.environ.get('DHCPD_CONF_FILE'))
    server_address = os.environ.get("SERVER_ADDRESS")
    server_app_address = os.environ.get("SERVER_PRIMARY_IP_ADDRESS")
    image_store = Path(os.environ.get("IMAGE_STORE"))
    boot_location = Path(os.environ.get("TFTP_SERVER_DST"))
    nfs_directory = Path(os.environ.get("NFS_SERVING_DIR"))
    fstab_config = Path(os.environ.get("FSTAB_CONF"))
    logging_file = Path(os.environ.get("LOGGING_FILE"))

