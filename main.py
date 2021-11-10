# This is a sample Python script.

import meraki
from abc import ABC, abstractmethod

dashboard = meraki.DashboardAPI('')
organization_id = ''


class Licenses(ABC):
    @abstractmethod
    def get_licenses(self):
        """Return a set of licenses"""


class UnassignedLicenses(Licenses):
    serial_filter: str = None

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def get_licenses(self):
        m_license = dashboard.organizations.getOrganizationLicenses
        return [item for item in m_license(organization_id, state='active', total_pages='all')
                if item['deviceSerial'] == self.serial_filter]


class Devices(ABC):
    @abstractmethod
    def get_devices(self):
        """Returns a list of devices"""


class UnlicensedDevices(Devices):
    license_expiration_filter: str = None

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def get_devices(self):
        m_device = dashboard.organizations.getOrganizationInventoryDevices
        return [item for item in m_device(organization_id, total_pages='all')
                if item['licenseExpirationDate'] == self.license_expiration_filter]


def assign_license(license_id, device_id=None):
    m_assign = dashboard.organizations.updateOrganizationLicense
    if device_id is not None:
        m_assign(organizationId=organization_id, licenseId=license_id, deviceSerial=device_id)
    else:
        m_assign(organizationId=organization_id, licenseId=license_id)


if __name__ == '__main__':
    licenses = UnassignedLicenses()
    devices = UnlicensedDevices()
    print(licenses.get_licenses())
    print(devices.get_devices())
