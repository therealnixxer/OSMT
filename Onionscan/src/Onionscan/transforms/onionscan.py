import json, subprocess, os, time

from canari.maltego.message import Entity, StringEntityField, IntegerEntityField, FloatEntityField, BooleanEntityField, DateEntityField
from canari.maltego.transform import Transform
from canari.maltego.entities import URL, Phrase, IPv4Address, EmailAddress, Domain
from canari.framework import EnableDebugWindow

import envVar, onionCli

@EnableDebugWindow
###################### DEFINE ENTITIES
class BtcAddress(Entity):
    _category_ = 'Personal'
    _namespace_ = 'PR'
    properties_btcaddress = StringEntityField('properties.btcaddress', display_name='BtcAddress', is_value=True)

class DomainEXT(Entity):
    _category_ = 'Infrastructure'
    _namespace_ = 'maltego'
    whois_info = StringEntityField('whois-info', display_name='WHOIS Info')
    fqdn = StringEntityField('fqdn', display_name='Domain Name', is_value=True)

#######################################
class onionService(Transform):
    """OnionScan Transform Hidden Service Name"""

    input_type = Domain

    def do_transform(self, request, response, config):
        Domain = request.entity.value
        pathToReports = envVar.pathToReports

        if os.path.isfile(pathToReports + Domain + ".scan"):
            data = json.loads(open(pathToReports + Domain + ".scan", "r").read())
        else:
            onionR = onionCli.onionRequest()
            jReport = onionR.do_get(Domain)
            data = json.loads(jReport)

        response += Phrase(str(data["hiddenService"]))
        return response

class onionDate(Transform):
    """OnionScan Transform dateScanned"""

    input_type = Domain

    def do_transform(self, request, response, config):
        Domain = request.entity.value
        pathToReports = envVar.pathToReports

        if os.path.isfile(pathToReports + Domain + ".scan"):
            data = json.loads(open(pathToReports + Domain + ".scan", "r").read())
        else:
            onionR = onionCli.onionRequest()
            jReport = onionR.do_get(Domain)
            data = json.loads(jReport)

        response += Phrase(data["dateScanned"])
        return response

class onionDetected(Transform):
    """OnionScan Transform Detected"""

    input_type = Domain

    def do_transform(self, request, response, config):
        Domain = request.entity.value
        pathToReports = envVar.pathToReports

        if os.path.isfile(pathToReports + Domain + ".scan"):
            data = json.loads(open(pathToReports + Domain + ".scan", "r").read())
        else:
            onionR = onionCli.onionRequest()
            jReport = onionR.do_get(Domain)
            data = json.loads(jReport)

        response  += Phrase("web: "      + str(data["webDetected"]))
        response  += Phrase("tls: "      + str(data["tlsDetected"]))
        response  += Phrase("ssh: "      + str(data["sshDetected"]))
        response  += Phrase("ricochet: " + str(data["ricochetDetected"]))
        response  += Phrase("irc: "      + str(data["ircDetected"]))
        response  += Phrase("ftp: "      + str(data["ftpDetected"]))
        response  += Phrase("smtp: "     + str(data["smtpDetected"]))
        response  += Phrase("bitcoin: "  + str(data["bitcoinDetected"]))
        response  += Phrase("mongodb: "  + str(data["mongodbDetected"]))
        response  += Phrase("vnc: "      + str(data["vncDetected"]))
        response  += Phrase("xmpp: "     + str(data["xmppDetected"]))
        response  += Phrase("skynet: "   + str(data["skynetDetected"]))
        return response

class onionPGPKeys(Transform):
    """OnionScan Transform PGPKeys"""

    input_type = Domain

    def do_transform(self, request, response, config):
        Domain = request.entity.value
        pathToReports = envVar.pathToReports

        if os.path.isfile(pathToReports + Domain + ".scan"):
            data = json.loads(open(pathToReports + Domain + ".scan", "r").read())
        else:
            onionR = onionCli.onionRequest()
            jReport = onionR.do_get(Domain)
            data = json.loads(jReport)

        response += Phrase(str(data["pgpKeys"]))
        return response

class onionIpAddress(Transform):
    """OnionScan Transform IP Address"""

    input_type = Domain

    def do_transform(self, request, response, config):
        Domain = request.entity.value
        pathToReports = envVar.pathToReports

        if os.path.isfile(pathToReports + Domain + ".scan"):
            data = json.loads(open(pathToReports + Domain + ".scan", "r").read())
        else:
            onionR = onionCli.onionRequest()
            jReport = onionR.do_get(Domain)
            data = json.loads(jReport)

        response += IPv4Address(str(data["identifierReport"]["ipAddresses"]))
        return response

class onionEmail(Transform):
    """OnionScan Transform Email"""

    input_type = Domain

    def do_transform(self, request, response, config):
        Domain = request.entity.value
        pathToReports = envVar.pathToReports

        if os.path.isfile(pathToReports + Domain + ".scan"):
            data = json.loads(open(pathToReports + Domain + ".scan", "r").read())
        else:
            onionR = onionCli.onionRequest()
            jReport = onionR.do_get(Domain)
            data = json.loads(jReport)

        try:
            for i in data["identifierReport"]["emailAddresses"]:
                response += EmailAddress(str(i))
        except:
            response += EmailAddress("None")
        return response

class onionBitcoin(Transform):
    """OnionScan Transform Bitcoin"""

    input_type = Domain

    def do_transform(self, request, response, config):
        Domain = request.entity.value
        pathToReports = envVar.pathToReports

        if os.path.isfile(pathToReports + Domain + ".scan"):
            data = json.loads(open(pathToReports + Domain + ".scan", "r").read())
        else:
            onionR = onionCli.onionRequest()
            jReport = onionR.do_get(Domain)
            data = json.loads(jReport)

        try:
            for i in data["identifierReport"]["bitcoinAddresses"]:
                response += BtcAddress(str(i))
        except:
            response += BtcAddress(str("None"))
        return response

class onionRelatedServices(Transform):
    """OnionScan Transform Related Onion Services"""

    input_type = Domain

    def do_transform(self, request, response, config):
        Domain = request.entity.value
        pathToReports = envVar.pathToReports

        if os.path.isfile(pathToReports + Domain + ".scan"):
            data = json.loads(open(pathToReports + Domain + ".scan", "r").read())
        else:
            onionR = onionCli.onionRequest()
            jReport = onionR.do_get(Domain)
            data = json.loads(jReport)

        try:
            for i in data["identifierReport"]["relatedOnionServices"]:
                response += DomainEXT(str(i))
        except:
            response += DomainEXT("none")
        return response

class onionRelatedDomains(Transform):
    """OnionScan Transform Related Onion Domains"""

    input_type = Domain

    def do_transform(self, request, response, config):
        Domain = request.entity.value
        pathToReports = envVar.pathToReports

        if os.path.isfile(pathToReports + Domain + ".scan"):
            data = json.loads(open(pathToReports + Domain + ".scan", "r").read())
        else:
            onionR = onionCli.onionRequest()
            jReport = onionR.do_get(Domain)
            data = json.loads(jReport)

        try:
            for i in data["identifierReport"]["relatedOnionDomains"]:
                response += DomainEXT(str(i))
        except:
            response += DomainEXT("None")
        return response
