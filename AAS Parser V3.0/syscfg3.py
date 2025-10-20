#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#けいけいし

import sys
sys.path.insert(0, ".")
sys.path.insert(1, "..")

import os
import argparse
import xmlschema
import asyncio
import xmltodict
import json

import xml.etree.ElementTree as ET

from asyncua import ua, Server
from asyncua.common.instantiate_util import instantiate
from asyncua.common.xmlexporter import XmlExporter


class AAS2OPCUA:
    def __init__(self, aas_file):
        print('---------- generating syscfg.json -------------------')
        print('>>> init()')

        self.aas_file = aas_file
        self.aas_schema = 'AAS.xsd'

        self.end_point = 'opc.tcp://0.0.0.0:4840/freeopcua/server/'

        self.doc = None
        self.root = None
        self.shells = None
        self.assets = None
        self.submodels = None
        self.descriptions = None

        self.server = None

        self.shell_info_list = []
        self.sm_info_list = []
        self.node_list = []

        self.gateway_list = []
        self.namespaces = []

        self.cloud_list = [] #2021.03.04 added




    async def create_opcua_server(self):
        print('>>> create_opcua_server()')

        self.server = Server()
        await self.server.init()
        self.server.set_endpoint(self.end_point)

        return True


    async def write_syscfg_json(self):
        with open('./generated/syscfg.json', mode='wt', encoding='utf-8') as f:

            f.write('{\n')
    
            # writing namespaces
            f.write('\t\"namespaces\":\n')
            f.write('\t[\n')

            ns_count = len(self.namespaces)
            for ns in self.namespaces:
                ns_count -= 1
                f.write('\t\t{ \"ns_index\":%d, \"ns\":\"%s\", \"aas_id\":\"%s\" }'%(ns['ns_index'], ns['ns_str'], ns['aas_str']))

                if(ns_count > 0):
                    f.write(',\n')
                else:
                    f.write('\n')
            # end of namespaces
            f.write('\t],\n')
    


            # writing system
            f.write('\t\"system\":\n')
            f.write('\t[\n')



# 2021.03.04 added #############################################################################################

            cloud_count = len(self.cloud_list)
            for cloud in self.cloud_list:
                cloud_count -= 1

                f.write('\t\t{\n')

                # writing gateway
                f.write('\t\t\t\"CloudName\": \"%s\",\n'%cloud['idShort'])

                for cloudcfg in cloud['config_list']:
                    if cloudcfg['idShort'] == '':
                        f.write('\t\t\t\"NetworkConnection\": \"%s\",\n'%cloudcfg['value'])
                        break

                for cloudcfg in cloud['config_list']:
                    if cloudcfg['idShort'] == 'SamplingInterval':
                        f.write('\t\t\t\"SamplingInterval\": \"%s\",\n'%cloudcfg['value'])
                        break
# #######################################################################################################




            gw_count = len(self.gateway_list)
            for gateway in self.gateway_list:
                gw_count -= 1

                f.write('\t\t{\n')

                # writing gateway
                f.write('\t\t\t\"GatewayName\": \"%s\",\n'%gateway['idShort'])

                for gwcfg in gateway['config_list']:
                    if gwcfg['idShort'] == 'NetworkConnection':
                        f.write('\t\t\t\"NetworkConnection\": \"%s\",\n'%gwcfg['value'])
                        break

                for gwcfg in gateway['config_list']:
                    if gwcfg['idShort'] == 'SamplingInterval':
                        f.write('\t\t\t\"SamplingInterval\": \"%s\",\n'%gwcfg['value'])
                        break

                
                # writing field-devices that will be connected with this gateway
                f.write('\t\t\t\"FieldDevices\" :\n')
                f.write('\t\t\t[\n')
            
                client_count = len(gateway['client_list'])
                for client in gateway['client_list']:
                    client_count -= 1

                    # begin of gateway-element
                    f.write('\t\t\t\t{\n')

                    f.write('\t\t\t\t\t\"DeviceName\": \"%s\",\n'%client['idShort'])

                    for clientcfg in client['config_list']:
                        if clientcfg['idShort'] == 'NetworkConnection':
                            f.write('\t\t\t\t\t\"NetworkConnection\": \"%s\",\n'%clientcfg['value'])
                            break

                    for clientcfg in client['config_list']:
                        if clientcfg['idShort'] == 'SamplingInterval':
                            f.write('\t\t\t\t\t\"SamplingInterval\": \"%s\"\n'%clientcfg['value'])
                            break


                    # writing client-pt-list
                    #f.write('\t\t\t\t\t\"ConnectedVariable\" :\n')
                    #f.write('\t\t\t\t\t[\n')
           
                    #pt_count = len(client['pt_list'])
                    #for pt in client['pt_list']:
                    #    pt_count -= 1
                    #    if pt_count > 0:
                    #        f.write('\t\t\t\t\t\t{ \"pt\": \"%s, %s, %s\" },\n'%(gateway['idShort'], client['idShort'], pt['value']))
                    #    else:
                    #        f.write('\t\t\t\t\t\t{ \"pt\": \"%s, %s, %s\" }\n'%(gateway['idShort'], client['idShort'], pt['value']))


                    #f.write('\t\t\t\t\t]\n')

                    # end of gateway-element
                    if client_count > 0:
                        f.write('\t\t\t\t},\n')
                    else:
                        f.write('\t\t\t\t}\n')

                # end of field-devices
                f.write('\t\t\t]\n')

                # end of gateway
                if gw_count > 0:
                    f.write('\t\t},\n')
                else:
                    f.write('\t\t}\n')

            # end of system
            f.write('\t]\n')

            # end of syscfg
            f.write('}')



    async def write_gwlist_csv(self):
        print('>>> write_gwlist_csv()')
        
        with open('./generated/gwlist.csv', mode='wt', encoding='utf-8') as f:
            for gateway in self.gateway_list:
                f.write(gateway['idShort'] + ',')
                f.write('ptmap_%s.csv'%gateway['idShort'] + ',')  
                
                for config in gateway['config_list']:
                    if config['idShort'] == 'NetworkConnection':
                            f.write(config['value'] + ',')
                            break;

                for config in gateway['config_list']:
                    if config['idShort'] == 'SamplingInterval':
                        f.write(config['value'])
                        break;

                f.write('\n')

    
    async def write_ptmaps_csv(self):
        print('>>> write_ptmaps_csv()')

        for gateway in self.gateway_list:
            with open('./generated/ptmap_%s.csv'%gateway['idShort'], mode='wt', encoding='utf-8') as f:
                for client in gateway['client_list']:
                    for pt in client['pt_list']:
                        f.write(str(client['c_index']) + ',')
                        f.write(pt['idShort'] + ',')
                        f.write(pt['value'] + ',')
                        f.write(' , 50.0\n')



    async def write_clients_csv(self):
        print('>>> write_clients.csv()')
        
        for gateway in self.gateway_list:
            with open('./generated/clients_%s.csv'%gateway['idShort'], mode='wt', encoding='utf-8') as f:
                for client in gateway['client_list']:
                    f.write(str(client['c_index']) + ',')
                    f.write(gateway['idShort'] + ',')
                    f.write(client['idShort'] + ',')
                    for config in client['config_list']:
                        if config['idShort'] == 'NetworkConnection':
                            f.write(config['value'] + ',')
                            break;
                    for config in client['config_list']:
                        if config['idShort'] == 'SamplingInterval':
                            f.write(config['value'])
                            break;

                    f.write('\n')


    async def add_aas_namespaces(self, ns_index, ns_str, aas_str):

        aas_ns = {}
        aas_ns['ns_index']  = ns_index
        aas_ns['ns_str']    = ns_str
        aas_ns['aas_str']   = aas_str

        self.namespaces.append(aas_ns)


    async def add_namespaces(self):
        print('>>> add_namespaces()')

        for shell_info in self.shell_info_list:
            shell_info['ns_index'] = await self.server.register_namespace(shell_info['ns_uri'])
            print('namespace[%d] = \'ns:%s\'' % (shell_info['ns_index'], shell_info['ns_uri']))

        return True


    async def load_aas(self):
        print('>>> load_aas(): %s' % (self.aas_file))

        if not os.path.exists(self.aas_file):
            print('%s does not exist!' % (self.aas_file))
            return False
 
        '''
        aas_xsd = xmlschema.XMLSchema(self.aas_schema)
        if aas_xsd.is_valid(self.aas_file) == False:
            print('aas[%s] has invalide schema format' % (self.aas_file))
            return False
        '''

        self.doc = ET.parse(self.aas_file)
        self.root = self.doc.getroot()
        for child in self.root:
            if child.tag.endswith('assetAdministrationShells'):
                self.shells = child
                print('shell')
            elif child.tag.endswith('assets'):
                self.assets = child
                print('asset')
            elif child.tag.endswith('submodels'):
                self.submodels = child
                print('submodes')
            elif child.tag.endswith('conceptDescriptions'):
                self.descriptions = None
                print('descriptions')

        return True

  
 

    async def parse_reference(self, shell_info, element, parent_tag):
        item_ref = {}
        for ref_elem in element:
            if ref_elem.tag.endswith('idShort'):
                item_ref['idShort'] = ref_elem.text

        if 'idShort' in item_ref:
            print('  reference: ' + parent_tag + '.' + item_ref['idShort'])



    async def parse_property(self, shell_info, element, parent_tag):
        item_property = {}
        for property_elem in element:
            if property_elem.tag.endswith('idShort'):
                item_property['idShort'] = property_elem.text
            elif property_elem.tag.endswith('valueType'):
                item_property['valueType'] = property_elem.text
            elif property_elem.tag.endswith('value'):
                item_property['value'] = property_elem.text

        if 'idShort' in item_property and 'valueType' in item_property:
            #print('  property: ' + parent_tag + '.' + item_property['idShort'])
            ns_index = shell_info['ns_index']
            tag_name = parent_tag + '.' + item_property['idShort']

            if shell_info['gwParsingLevel'] == 3:   # BasicConfig of 'rempte client'
                basic_config = {}
                basic_config['idShort'] = item_property['idShort']
                basic_config['valueType'] = item_property['valueType']
                basic_config['value'] = item_property['value']

                shell_info['remote_client']['config_list'].append(basic_config)
                print('    - client-config: ' + basic_config['idShort'] + ' = ' + basic_config['value'])

            elif shell_info['gwParsingLevel'] == 4: # ConnectedVariable
                opcua_tag = {}
                opcua_tag['idShort'] = item_property['idShort']
                opcua_tag['value'] = item_property['value']

                shell_info['remote_client']['pt_list'].append(opcua_tag)
                print('    - opcua-point: ' + opcua_tag['idShort'] + ' = ' + opcua_tag['value'])
            
            elif shell_info['gwParsingLevel'] == 5:   # BasicConfig of 'Edge gateway'
                basic_config = {}
                basic_config['idShort'] = item_property['idShort']
                basic_config['valueType'] = item_property['valueType']
                basic_config['value'] = item_property['value']

                shell_info['edge_gw']['config_list'].append(basic_config)
                print('  - edge-config: ' + basic_config['idShort'] + ' = ' + basic_config['value'])

            #self.aasvar_list.append("ns=%d;s=%s"%(ns_index, tag_name))
    


    async def parse_collection(self, shell_info, element, parent_tag):
        item_collection = {}
        for coll_elem in element:
            if coll_elem.tag.endswith('idShort'):
                item_collection['idShort'] = coll_elem.text

        if 'idShort' in item_collection:
            ns_index = shell_info['ns_index']
            tag_name = parent_tag + '.' + item_collection['idShort']
            browse_name = '%d:%s'%(ns_index, item_collection['idShort'])

            if shell_info['gwParsingLevel'] != 5:
                if item_collection['idShort'] == 'BasicConfiguration':
                    shell_info['gwParsingLevel'] = 3                    
                elif item_collection['idShort'] == 'ConnectedVariable':
                    shell_info['gwParsingLevel'] = 4

            for coll_elem in element:
                if coll_elem.tag.endswith('value'):
                    
                    #for sm_elem in coll_elem:
                        #if sm_elem.tag.endswith('submodelElement'):
                    for sm_elem_item in coll_elem:
                        if sm_elem_item.tag.endswith('submodelElementCollection'):
                            await self.parse_collection(shell_info, sm_elem_item, tag_name)
                        
                        elif sm_elem_item.tag.endswith('property'):
                            await self.parse_property(shell_info, sm_elem_item, tag_name)
                        
                        elif sm_elem_item.tag.endswith('referenceElement'):
                            await self.parse_reference(shell_info, sm_elem_item, tag_name)

    async def parse_tag_from_element(self, element, tagname):
        for elem_item in element:
            if(elem_item.tag.endswith(tagname)):
                    return elem_item.text

        return None

    async def parse_sm_elements(self, shell_info, sm_elements, parent_tag):
        # parsing 'edge-gateways' list

        for sm_elem_item in sm_elements:
            if sm_elem_item.tag.endswith('submodelElementCollection'):

                elem_item_idshort = await self.parse_tag_from_element(sm_elem_item, 'idShort')
                if elem_item_idshort == None:
                    continue;

                # parsing new 'edge-gateway'
                ns_index = shell_info['ns_index']
                tag_name = parent_tag + '.' + elem_item_idshort
                browse_name = '%d:%s'%(ns_index, elem_item_idshort)

                edge_gw = {}
                edge_gw['idShort'] = elem_item_idshort
                edge_gw['c_index'] = 0
                edge_gw['client_list'] = []
                edge_gw['config_list'] = []

                self.gateway_list.append(edge_gw)

                shell_info['edge_gw'] = edge_gw
                print('edge-gateway: ' + edge_gw['idShort'])



                #searching sub-nodes
                for sub_elem_item in sm_elem_item:
                    # sub_elem.tag list:
                    #  - subelement tag: {http://www.admin-shell.io/aas/2/0}idShort
                    #  - subelement tag: {http://www.admin-shell.io/aas/2/0}semanticId
                    #  - subelement tag: {http://www.admin-shell.io/aas/2/0}kind
                    #  - subelement tag: {http://www.admin-shell.io/aas/2/0}qualifier
                    #  - subelement tag: {http://www.admin-shell.io/aas/2/0}value

                    if sub_elem_item.tag.endswith('value'):
                        #print(sub_elem.text)
                        #for sub_elem_item in sub_elem:
                        #print("=="+sub_elem_item[0].text)
                        #print('   sub-elem-item: ' + sub_elem_item.tag)
                        #if sub_elem_item.tag.endswith('submodelElement'):

                        for gw_component in sub_elem_item:
                            # parsing 'BasicConfig' or 'Remote Clients'
                            gw_component_idshort = await self.parse_tag_from_element(gw_component, 'idShort')
                            if gw_component_idshort == None:
                                continue;

                            if gw_component_idshort == 'BasicConfiguration':
                                shell_info['gwParsingLevel'] = 5
                                await self.parse_collection(shell_info, gw_component, tag_name)
                                
                            else:
                                ns_index = shell_info['ns_index']
                                tag_name = parent_tag + '.' + gw_component_idshort
                                browse_name = '%d:%s'%(ns_index, gw_component_idshort)

                                remote_client = {}
                                remote_client['edge_gw'] = shell_info['edge_gw']
                                remote_client['idShort'] = gw_component_idshort
                                remote_client['c_index'] = shell_info['edge_gw']['c_index']
                                remote_client['config_list'] = []
                                remote_client['pt_list'] = []

                                shell_info['edge_gw']['c_index'] += 1
                                shell_info['edge_gw']['client_list'].append(remote_client)
                                shell_info['remote_client'] = remote_client

                                print('  - remote-client: ' + remote_client['idShort'])
                                
                                shell_info['gwParsingLevel'] = 2
                                await self.parse_collection(shell_info, gw_component, tag_name)

                        #await self.parse_collection(shell_info, sm_elem_item, tag_name)


                '''
                for sm_elem_item in sm_elem:
                    if sm_elem_item.tag.endswith('submodelElementCollection'):
                        await self.parse_collection(shell_info, sm_elem_item, parent_tag)
                    
                    elif sm_elem_item.tag.endswith('property'):
                        await self.parse_property(shell_info, sm_elem_item, parent_tag)
                    
                    elif sm_elem_item.tag.endswith('referenceElement'):
                        await self.parse_reference(shell_info, sm_elem_item, parent_tag)
                '''





    async def parse_sm(self, shell_info, sm, parent_tag):



        print('>>> parse_sm()')


        #parsing 'EdgeGWSolution' <== Submodel

        sm_info = {} #submodel
        sm_info['aas'] = shell_info

        for sm_elem in sm:
            if sm_elem.tag.endswith('id'):
                sm_info['identification'] = sm_elem.text
            
            elif sm_elem.tag.endswith('idShort'):
                sm_info['idShort'] = sm_elem.text
                sm_info['tagName'] = shell_info['idShort'] + '.' + sm_info['idShort']


        if 'identification' in sm_info and 'idShort' in sm_info:

            #print('AAS: ' + shell_info['idShort'] + ' (' + shell_info['identification'] + ')')
            ns_index = shell_info['ns_index']
            tag_name = parent_tag + '.' + sm_info['idShort']
            browse_name = '%d:%s'%(ns_index, sm_info['idShort'])
            
            for sm_elements in sm:
                if sm_elements.tag.endswith('submodelElements'):
                    #sm_info == 'EdgeGWSolution' submodel
                    #print('parsing submodelElements: ' + sm_info['tagName'] + '(' + sm_info['identification'] + ')')
                    await self.parse_sm_elements( shell_info, sm_elements, tag_name)

        return True






    async def parse_sm_refs(self, shell_info, sm_refs):

        shell_info['sm_id_list'] = []

        for sm_ref in sm_refs:
            shell_info['sm_list'] = []
            for sm_ref_elem in sm_ref:
                if sm_ref_elem.tag.endswith('keys'):
                    for key in sm_ref_elem:
                        shell_info['sm_id_list'].append(key[1].text)







    async def parse_aas(self):
        print('parse_aas()')

        if self.shells == None:
            return False

        # add open62541 default namespace
        await self.server.register_namespace('urn:open62541.server.application')
        await self.add_aas_namespaces(1, 'urn:open62541.server.application', '-')

        # add data-acquisition-solution default namespace
        kosmo_nid = 2
        await self.add_aas_namespaces(2, 'https://www.smart-factory.kr/datasolution', '-')
        #ns_index = 2

        for shell in self.shells:
            shell_info = {} # AAS

            for shell_elem in shell:
                if shell_elem.tag.endswith('idShort'):
                    shell_info['idShort'] = shell_elem.text
                elif shell_elem.tag.endswith('id'):
                    shell_info['identification'] = shell_elem.text
                elif shell_elem.tag.endswith('submodels'):
                    await self.parse_sm_refs(shell_info, shell_elem)


            if 'idShort' in shell_info and 'identification' in shell_info:
                
                shell_info['ns_index'] = kosmo_nid
                shell_info['browse_name'] =  '%d:%s'%(shell_info['ns_index'], shell_info['idShort'])



                if shell_info['identification'] != 'http://www.aasnest.io/ids/aas/CloudDataSolution':
                    continue;

                if 'sm_id_list' in shell_info:

                    # this AAS contains submodel that start with 'OperationalData'
                    # parsing submodels & elements of AAS
                    for sm_id in shell_info['sm_id_list']:
                    
                    

                        if sm_id != 'http://www.aasnest.io/ids/sm/EdgeGWSolution':
                            continue
                        
                        # search xml position for submodel
                        aas_sm_elem = None
                        for sm in self.submodels:
                            for sm_elem in sm:
                                if sm_elem.tag.endswith('id') and sm_elem.text == sm_id:
                                    aas_sm_elem = sm
                                    break

                        # parsing & add
                        if aas_sm_elem != None:
                            shell_info['gwParsingLevel'] = 0    # 0(gateway-list) 1(client-list) 2(under-client) 3(client-config) 4(client-pt-list)
                            parent_tag = shell_info['idShort']
                            await self.parse_sm(shell_info, aas_sm_elem, parent_tag)




        return True







    async def convert_model(self):
        print('convert_model()')

        await self.create_opcua_server()
        await self.load_aas()
        await self.parse_aas()
        #await self.write_clients_csv()
        #await self.write_ptmaps_csv()
        #await self.write_gwlist_csv()
        await self.write_syscfg_json()
        return True


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--aas')
    #parser.add_argument('--opcua')
    args = parser.parse_args()
    print(args)

    if args.aas == None:
        print('usage: main.py [-h] [--aas AAS]')
        exit()

    modeler = AAS2OPCUA(args.aas)
    await modeler.convert_model()

if __name__ == '__main__':
    asyncio.run(main())

