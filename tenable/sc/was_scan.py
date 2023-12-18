"""
WAS Scan
==========

The following methods allow for interaction into the Tenable Security Center
:sc-api:`WAS Scan <WAS-Scan.htm>` API.  These items are typically seen under
the **WAS Scan** section of Tenable Security Center.

Methods available on ``sc.was_scan``:

.. rst-class:: hide-signature
.. autoclass:: WasScanAPI
    :members:

"""
from pprint import pprint
from typing import List, Optional, Any

from tenable.sc.base import SCEndpoint


def _to_boolean_string(boolean_value: bool) -> str:
    """
    Returns a boolean string representation of a python Boolean value.
    True returns "true", False returns "false"

    Args:
        boolean_value:

    Returns: str

    """
    return "true" if boolean_value else "false"


class WasScanAPI(SCEndpoint):
    api_route = "wasScan"

    def _build_creation_or_update_request(self, **kwargs: Any) -> dict:
        """
        Builds and returns the request object for an SC WAS Scan creation.
        Note: we're converting numbers to strings in this function as the API requires it to be a string.
        Args:
            **kwargs: Properties in the WAS Scan creation request.

        Returns: dict
        """
        request = dict()

        if kwargs["name"]:
            request["name"] = self._check("name", kwargs["name"], str)

        if "type" in kwargs:
            request["type"] = self._check("type", kwargs["type"], str)

        if "description" in kwargs:
            request["description"] = self._check("description", kwargs["description"], str)

        if "repository_id" in kwargs:
            request["repository"] = {
                "id": str(kwargs["repository_id"])
            }

        if "zone_id" in kwargs:
            request["zone"] = {
                "id": str(kwargs["zone_id"])
            }

        if "dhcpTracking" in kwargs:
            request["dhcpTracking"] = _to_boolean_string(kwargs["dhcpTracking"])

        if "classifyMitigatedAge" in kwargs:
            request["classifyMitigatedAge"] = str(kwargs["classifyMitigatedAge"])

        if "schedule_type" in kwargs:
            request["schedule"] = {
                "type": self._check("schedule_type", kwargs["schedule_type"], str,
                                    choices=["ical", "never", "rollover", "template"])
            }

        if "reports" in kwargs:
            reports = kwargs["reports"]
            if len(reports) > 0:
                request["reports"] = [
                    {
                        "id": self._check("report_id", report[0], int),
                        "reportSource": self._check("reportSource", report[1], str,
                                                    choices=["cumulative", "patched", "individual", "lce", "archive",
                                                             "mobile"])
                    } for report in reports
                ]

        if "assets" in kwargs:
            assets = kwargs["assets"]
            if len(assets) > 0:
                request["assets"] = [
                    {
                        "id": self._check("asset", asset, int)
                    } for asset in assets
                ]

        if "credentials" in kwargs:
            credentials = kwargs["credentials"]
            if len(credentials) > 0:
                request["credentials"] = [
                    {
                        "id": self._check("credentials", credential, int)
                    } for credential in credentials
                ]

        if "emailOnLaunch" in kwargs:
            request["emailOnLaunch"] = _to_boolean_string(kwargs["emailOnLaunch"])

        if "emailOnFinish" in kwargs:
            request["emailOnFinish"] = _to_boolean_string(kwargs["emailOnFinish"])

        if "timeoutAction" in kwargs:
            request["timeoutAction"] = self._check("timeoutAction",
                                                   kwargs["timeoutAction"],
                                                   str,
                                                   choices=["discard", "import", "rollover"]
                                                   )

        if "scanningVirtualHosts" in kwargs:
            request["scanningVirtualHosts"] = _to_boolean_string(kwargs["scanningVirtualHosts"])

        if "rolloverType" in kwargs:
            request["rolloverType"] = self._check("rolloverType",
                                                  kwargs["rolloverType"],
                                                  str,
                                                  choices=["nextDay", "template"]
                                                  )
        if "urlList" in kwargs:
            request["urlList"] = self._check("urlList", kwargs["urlList"], str)

        if "maxScanTime" in kwargs:
            request["maxScanTime"] = str(kwargs["maxScanTime"])

        return request

    def create(self, **kwargs):
        """
        Creates a WAS Scan depending on access and permissions.

        :sc-api:`was-scan: list <Was-Scan.htm#wasScan_POST>`

        Args:
            name (str):
                The name of the scan.
            type (str, optional):
                Type of the scan.
            description (str, optional):
                A description for the scan zone.
            repository_id (int):
                Repository ID.
            zone_id (int, optional):
                Zone ID.
            dhcpTracking (boolean, optional):
                Scould Security Center do DHCP Tracking?
            classifyMitigatedAge (int, optional):
                Classify Mitigated Age
            schedule_type (str, optional):
                Schedule Type includes  "dependent" | "ical" | "never" | "rollover" | "template"
            reports (list, optional):
                This is a List of Tuples of 2 elements. The first element in the tuple should be a number (ID)
                and the last/second element should be a string (reportSource). It can be one of these strings.
                "cumulative" | "patched" | "individual" | "lce" | "archive" | "mobile"
            assets: (list, optional):
                List of Asset IDs.
            credentials (list, optional):
                List of Credential IDs.
            emailOnLaunch (boolean, optional):
                Should we send an email on launch?
            emailOnFinish (boolean, optional):
                Should we send an email upon completion of the scan?
            timeoutAction (str, optional):
                Time out action can be one of these: "discard" | "import" | "rollover"
            scanningVirtualHosts (boolean, optional):
                Should we scan Virtual Hosts?
            rolloverType (str, optional):
                Rollover type should be one of these: "nextDay" | "template"
            urlList (str, optional)
                Valid URL List
            maxScanTime (int, optional)
                Max Scan Time

        Returns:
            :obj:`dict`:
                The newly created WAS Scan.

        Examples:
            >>> zone = sc.was_scan.create(name="Example Scan")
        """
        request = self._build_creation_or_update_request(**kwargs)
        return self._api.post(self.api_route, json=request).json()['response']

    def list(self, fields: Optional[List[str]] = None):
        """
        Retrieves the list of WAS Scans.

        :sc-api:`was-scan: list <Was-Scan.htm#wasScan_GET>`

        Args:
            fields (list, optional):
                A list of attributes to return for each scan.

        Returns:
            :obj:`list`:
                A list of WAS Scans.

        Examples:
            >>> for scan in sc.was_scan.list():
            ...     pprint(scan)
        """
        params = {}
        if fields:
            string_fields = [self._check("fields", f, str) for f in fields]
            params["fields"] = ",".join(string_fields)

        return self._api.get(self.api_route, params=params).json()['response']

    def details(self, scan_id: Optional[str] = None, fields: Optional[List[str]] = None) -> dict:
        """
        Retrieves the details of the given WAS Scan.

        :sc-api:`was-scan: list <Was-Scan.htm#WASScanRESTReference-/wasScan/{id}>`

        Args:
            scan_id (str, optional):
                ID of the WAS scan to be fetched.
            fields (list, optional):
                A list of attributes to return for the scan.

        Returns:
            :obj:`dict`:
                The details of the WAS scan.

        Examples:
            >>> sc.was_scan.details(1)
        """

        params = {}
        if fields:
            string_fields = [self._check("fields", f, str) for f in fields]
            params["fields"] = ",".join(string_fields)

        return self._api.get(f"{self.api_route}/{scan_id}", params=params).json()['response']

    def edit(self, scan_id: str, **kwargs) -> dict:
        """
        Updates a WAS Scan depending on access and permissions.

        :sc-api:`was-scan: list <Was-Scan.htm#wasScan_uuid_PATCH>`

        Args:
            scan_id (str):
                ID of the scan whose parameters need to be edited.
            name (str):
                The name of the scan.
            type (str, optional):
                Type of the scan.
            description (str, optional):
                A description for the scan zone.
            repository_id (int):
                Repository ID.
            zone_id (int, optional):
                Zone ID.
            dhcpTracking (boolean, optional):
                Scould Security Center do DHCP Tracking?
            classifyMitigatedAge (int, optional):
                Classify Mitigated Age
            schedule_type (str, optional):
                Schedule Type includes  "dependent" | "ical" | "never" | "rollover" | "template"
            reports (list, optional):
                This is a List of Tuples of 2 elements. The first element in the tuple should be a number (ID)
                and the last/second element should be a string (reportSource). It can be one of these strings.
                "cumulative" | "patched" | "individual" | "lce" | "archive" | "mobile"
            assets: (list, optional):
                List of Asset IDs.
            credentials (list, optional):
                List of Credential IDs.
            emailOnLaunch (boolean, optional):
                Should we send an email on launch?
            emailOnFinish (boolean, optional):
                Should we send an email upon completion of the scan?
            timeoutAction (str, optional):
                Time out action can be one of these: "discard" | "import" | "rollover"
            scanningVirtualHosts (boolean, optional):
                Should we scan Virtual Hosts?
            rolloverType (str, optional):
                Rollover type should be one of these: "nextDay" | "template"
            urlList (str, optional)
                Valid URL List
            maxScanTime (int, optional)
                Max Scan Time

        Returns:
            :obj:`dict`:
                The edited WAS Scan

        Examples:
            >>> zone = sc.was_scan.edit(scan_id=1, name="Example Scan")
        """
        request = self._build_creation_or_update_request(**kwargs)
        return self._api.patch(f"{self.api_route}/{scan_id}", json=request).json()['response']

    def delete(self, scan_id: str) -> dict:
        """
        Deletes the given WAS Scan.

        :sc-api:`was-scan: list <Was-Scan.htm#wasScan_uuid_DELETE>`

        Args:
            scan_id (str, optional):
                ID of the WAS scan to be fetched.

        Returns:
            :obj:`dict`:
                A deletion response.

        Examples:
            >>> sc.was_scan.delete(scan_id=1)
        """
        return self._api.delete(f"{self.api_route}/{scan_id}").json()

    def copy(self, scan_id: Optional[int] = None, scan_uuid: Optional[str] = None, name: str = None):
        """
        Copies the WAS Scan associated with {id} or {uuid}, depending on access and permissions.

        :sc-api:`was-scan: list <Was-Scan.htm#wasScan_uuid_DELETE>`

        Args:
            name (str):
                Name of the scan.
            scan_id (int, optional):
                ID of the WAS scan to be copied.
            scan_uuid (str, optional):
                UUID of the WAS scan to be copied.

        Returns:
            :obj:`dict`:
                A Copy response.

        Examples:
            >>> sc.was_scan.copy(scan_id=1)
        """

        if (scan_id is not None and scan_uuid is not None) or (scan_id is None and scan_uuid is None):
            raise ValueError("Exactly one of these [scan_id, scan_uuid] should be found.")

        request = {
            "name": self._check("name", name, str),
            "targetUser": {

            }
        }

        path = None

        if scan_id:
            request["targetUser"]["id"] = self._check("scan_id", scan_id, int)
            path = f"{self.api_route}/{scan_id}/copy"
        else:
            request["targetUser"]["uuid"] = self._check("scan_uuid", scan_uuid, str)
            path = f"{self.api_route}/{scan_uuid}/copy"

        return self._api.post(path, json=request).json()['response']