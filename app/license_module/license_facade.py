from .license_models import License
from app.extensions import db
from app.logging import logger as log
from app.utils import (
    LICENSE_REGISTERED,
    LICENSE_UNREGISTERED,
    LICENSE_WRONG_CLUSTER,
    LICENSE_DOESNT_EXIST,
)

class LicenseFacade:
    def add_license(self, certificate, pods):
        if certificate and pods:
            if self.get_license_status('', certificate) == LICENSE_DOESNT_EXIST:
                try:
                  newLicense = License(
                    certificate=certificate,
                    cluster_id='',
                    pods=pods,
                  )
                  db.session.add(newLicense)
                  db.session.commit()
                  return {"status": True}
                except Exception as e:
                  log.info('Failed to add license')
                  log.exception(e)
            else:
                return {"status": False, "error": "Already exist"}
        else:
            return {"status": False, "error": "Check parameters"}

    def register_license(self, certificate, cluster_id):
        if certificate and cluster_id is not None:
            current_license = License.query.filter_by(certificate=certificate).first()
            license_status = self.get_license_status(cluster_id, certificate)

            if license_status == LICENSE_REGISTERED:
                return {"status": False, "pods": current_license.pods, "error": "Already registered"}
            elif  license_status == LICENSE_DOESNT_EXIST:
                return {"status": False, "pods": 0, "error": "Certificate not found"}
            elif license_status == LICENSE_UNREGISTERED:
                try:
                    current_license.cluster_id = cluster_id
                    db.session.commit()
                    return {"status": True, "pods": current_license.pods}
                except Exception as e:
                  log.info('Failed to register license')
                  log.exception(e)
        else:
            return {"status": False, "pods": 0, "error": "Check params"}
    
    def check_license(self, certificate, cluster_id):
        if certificate is not None and cluster_id is not None:
            license_status = LicenseFacade.get_license_status(cluster_id, certificate)
            license_pods = LicenseFacade.get_licence_pods(certificate)
            return {"status": license_status, "pods": license_pods}
        else:
            return {"status": False, "error": "Check parameters"}

    @staticmethod
    def get_license_status(cluster_id, certificate):
        if not certificate:
            return LICENSE_DOESNT_EXIST
        else:
            license = License.query.filter_by(certificate=certificate).first()
            if license:
                if license.cluster_id:
                    if license.cluster_id == cluster_id:
                        return LICENSE_REGISTERED
                    else:
                        return LICENSE_WRONG_CLUSTER
                else:
                    return LICENSE_UNREGISTERED
            else:
                return LICENSE_DOESNT_EXIST

    @staticmethod
    def get_licence_pods(certificate):
        if not certificate:
            return 0

        license = License.query.filter_by(certificate=certificate).first()
        if license:
            return license.pods
        else:
            return 0
