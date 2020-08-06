#!/usr/bin/env python
# Filename: xml_rw.py 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 11 May, 2016
"""

import sys,os,time
import io_function,basic
import xml.etree.ElementTree as ET
# from lxml import etree as ET
from xml.etree.ElementTree import ParseError
import xml.dom.minidom as minidom

class XmlClass(object):
    """
    create or phrase a xml file, when the class object is deleted from memory, it will be saved to disk
    """
    def __init__(self,xml_path):
        self.meta_path = xml_path
        self.tree = None
        self.root = None
    def __del__(self):
        if self.tree  is not None:
            self.save_xml()

    def save_xml(self):
        # transform xml format, then the xml file look nice in multi line
        if os.path.isfile(self.meta_path) is False:
            root_str = self.prettify(self.root)
            self.root = ET.fromstring(root_str)
            self.tree = ET.ElementTree(self.root)

        # self.__tree = ET.ElementTree(self.__root)
        self.tree.write(self.meta_path, encoding='UTF-8')


    def phrase_xml(self):
        """
        phrase xml file
        Returns:True if successful, False Otherwise

        """

        meta_path = self.meta_path
        if io_function.is_file_exist(meta_path) is False:
            assert False
        try:
            self.tree = ET.parse(meta_path)
            self.root = self.tree.getroot()
        except ParseError:
            basic.outputlogMessage(str(ParseError))
            basic.outputlogMessage('open %s failed'%meta_path)
            assert False

        if self.tree is None or self.root is None:
            basic.outputlogMessage('parse %s failed'%meta_path)
            assert False

    def create_xml(self,root_tag):
        """
        create pre-processing  metadata
        Returns:True if successful, False Otherwise

        """
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.root = ET.Element(root_tag)
        self.create_sub_element(self.root,'createTime',text=time_str)
        self.tree = ET.ElementTree(self.root)
        return True

    def prettify(self,elem):
        """
        Return a pretty-printed XML string for the Element
        Args:
            elem:

        Returns:A string contains xml information

        """
        rough_string = ET.tostring(elem, 'UTF-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")

    def create_element(self,tag,text='',attrib=None):
        """
        create a element object
        Args:
            tag: element tag name
            text: element text
            attrib: attrib value store in dict variable, eg {'a':'1','b':'2'}

        Returns:the element object

        """
        element = ET.Element(tag)
        if len(text)>1:
            element.text = text
        if attrib is not None:
            element.attrib = attrib
        return element

    def create_sub_element(self, parent,tag, text='', attrib=None):
        """
        create a child element of 'parent' element
        Args:
            parent: the parent node
            tag:element tag name
            text:element text
            attrib:attrib value store in dict variable, eg {'a':'1','b':'2'}

        Returns:the element object

        """
        element = ET.SubElement(parent,tag)
        if len(text)>0:
            element.text = text
        if attrib is not None:
            element.attrib = attrib
        return element

    def set_element_text(self,tag, text=''):
        """
        set text in root level
        Args:
            tag:tag name of this node
            text:tag text of this node

        Returns:None

        """
        node_list = self.get_element(tag)
        if len(node_list) < 1:
            self.create_sub_element(self.root, tag, text=text)
        else:
            node_list[0].text = text

    def set_sub_element(self,parent_name,tag,text='',attrib=None):
        parent_node_list = self.get_element(parent_name)
        if len(parent_node_list)==1:
            node_list = self.get_sub_element(parent_node_list[0],tag)
            if len(node_list) < 1:
                self.create_sub_element(parent_node_list[0], tag, text=text)
            else:
                node_list[0].text = text
                # node_list[0].attrib =
            return True
        else:
            basic.outputlogMessage('the number of %s node is 0 or greater than 1'%parent_name)
            assert False


    def add_element(self,parent_name,tag, text='', attrib=None):
        parent_node_list = self.get_element(parent_name)
        if len(parent_node_list)==1:
            self.create_sub_element(parent_node_list[0], tag, text=text, attrib=attrib)
            return True
        else:
            basic.outputlogMessage('the number of %s node is 0 or greater than 1'%parent_name)
            assert False


    def get_element(self,element_tag):
        """
        get element object list
        Args:
            element_tag:element tag

        Returns:element object list

        """
        return self.get_sub_element(self.root,element_tag)

    def get_sub_element_text_with_p_tag(self,parent_tag,element_tag):
        node_list = self.get_element(parent_tag)
        if len(node_list) != 1:
            basic.outputlogMessage('the number of is not 1'%parent_tag)
            assert False
        return self.get_sub_element_text(node_list[0],element_tag)

    def get_sub_element_text(self, parent, element_tag):
        element_list = parent.findall(element_tag)
        text_list = []
        for element in element_list:
            text_list.append(element.text)
        return text_list

    def get_sub_element(self,parent,element_tag):
        element_list = parent.findall(element_tag)
        return element_list


    def get_element_text(self,element_tag):
        """
        get the element text from whole xml file
        Args:
            element_tag:element tag

        Returns: a list datum contains all elements whose tag is element_tag

        """
        return self.get_sub_element_text(self.root,element_tag)

    def get_sub_element_text(self,parent,element_tag):
        """
        get the child element text
        Args:
            parent: the parent node
            element_tag:element tag

        Returns:a list datum contains all elements whose tag is element_tag

        """
        element_list = parent.findall(element_tag)
        text_list = []
        for element in element_list:
            text_list.append(element.text)
        return text_list




class ImgProMetaDataClass(XmlClass):
    """
    store pre-processing information with one image output
    """
    def __init__(self,meta_path):
        super(ImgProMetaDataClass,self).__init__(meta_path)
        # print self.meta_path
        if os.path.isfile(meta_path):
            self.phrase_xml()
        else:
            self.create_xml('Pre-processing')

    def __del__(self):
        super(ImgProMetaDataClass,self).__del__()
        pass

    def create_xml(self,root_tag):
        super(ImgProMetaDataClass,self).create_xml(root_tag)
        self.create_sub_element(self.root,'original_files')
        self.create_sub_element(self.root, 'original_images')
        self.create_sub_element(self.root, 'original_metas')
        self.create_sub_element(self.root, 'reprojected_images')


        # element = self.create_element('orginal_file',text='/home/hlc1.tif',attrib={'aa':'a',"bb":'b'})
        # element2 = self.create_sub_element(self.root,'original_file',text='/home/2.tif')
        # self.root.append(element)

    # def save_xml(self,b_keep_mid_file):
    #     """
    #     save xml file and clear some middle files
    #     Args:
    #         b_keep_mid_file:
    #
    #     Returns:True
    #
    #     """
    #     super(ImgProMetaDataClass, self).save_xml()
    #     #clear middle files


    def get_product_metadata_file_path(self):
        """
        get the product metadata path(if there are multi metadata files ,select the first one)
        Returns:the first metadata file path, False otherwise

        """
        metadata_path_list =  self.get_sub_element_text_with_p_tag('original_metas','metapath')
        assert os.path.isfile(metadata_path_list[0])
        return os.path.isfile(metadata_path_list[0])

    def get_orginal_file_list(self):
        """
        get the original files(LC***.gz) list
        Returns: a list stored original files

        """
        file_list = self.get_sub_element_text_with_p_tag('original_files','original_file')
        return file_list

    def get_orginal_image_list(self):
        """
        get the original image files(LE7****.tif) list
        Returns:a list stored original image files

        """
        images_list = self.get_sub_element_text_with_p_tag('original_images','original_image')
        return images_list

    def get_reprojected_image_list(self):
        reproject_list =  self.get_sub_element_text_with_p_tag('reprojected_images','original_image')
        return reproject_list

    def get_product_path(self):
        """
        get the product path (assume only one product file)
        Returns:product path if exist, '' otherwise

        """
        product_path = self.get_element_text('product_path')
        if len(product_path) <1:
            return ''
        if len(product_path)>1:
            basic.outputlogMessage('the product number exceed 1')
            assert False
        if os.path.isfile(product_path[0]) is False:
            return ''
        return product_path[0]

    def set_product_path(self, product_image):
        node_list = self.get_element('product_path')
        if len(node_list)<1:
            self.create_sub_element(self.root,'product_path',text=product_image)
        else:
            node_list[0].text = product_image


    def set_base_preProcess_info(self,data_satellite,b_keep_mid_file,band_used,work_dir,pre_processing_dir,projection):
        self.create_sub_element(self.root, 'work_dir', text=str(work_dir))
        self.create_sub_element(self.root, 'pre_processing_dir', text=str(pre_processing_dir))
        self.create_sub_element(self.root, 'data_satellite', text=str(data_satellite))
        self.create_sub_element(self.root, 'keep_mid_file', text=str(b_keep_mid_file))
        self.create_sub_element(self.root, 'band_used', text=str(band_used))
        self.create_sub_element(self.root, 'projection', text=str(projection))

    # def set_band_used(self,used_band):
    #     self.create_sub_element(self.root,'image_band_used',text=str(used_band))

    def add_original_file(self,file_path):
        self.add_element('original_files','original_file',text=file_path)

    def add_original_image(self,image_path):
        self.add_element('original_images', 'original_image', text=image_path)

    def add_reprojected_image(self, prj_image):
        self.add_element('reprojected_images', 'reprojected_image', text=prj_image)

    def add_metadata_file_path(self,meta_path):
        self.add_element('original_metas', 'metapath', text=meta_path)





class OffsetMetaDataClass(XmlClass):
    def __init__(self,xml_path):
        super(OffsetMetaDataClass,self).__init__(xml_path)
        # print self.meta_path
        if os.path.isfile(xml_path):
            self.phrase_xml()
        else:
            self.create_xml('Getting_Offset')

    def __del__(self):
        super(OffsetMetaDataClass,self).__del__()
        pass

    def create_xml(self,root_tag):
        super(OffsetMetaDataClass,self).create_xml(root_tag)
        self.create_sub_element(self.root, 'coregistration')
        self.create_sub_element(self.root, 'terrain_offset')
        self.create_sub_element(self.root, 'subset')
        self.create_sub_element(self.root, 'feature_tracking')

    def get_fea_images_product(self):
        """
        get file paths of feature image
        Returns:(feature image1, feature image2)

        """
        image1 = self.get_element_text('feature_image1')
        image2 = self.get_element_text('feature_image2')
        if len(image1) == 1 and len(image2) == 1:
            return image1[0], image2[0]
        elif len(image1) == 0 or len(image2) == 0:
            basic.outputlogMessage('feature image1 or image2  not exist')
            return '', ''
        else:
            basic.outputlogMessage('the count of feature image1 or image2 is not 1')
            assert False


    def set_fea_images_product(self,fea_image1,fea_image2):
        """
        set file paths of feature images
        Args:
            fea_image1: the path of feature image1
            fea_image2: the path of feature image2

        Returns:True

        """
        self.set_element_text('feature_image1',text=fea_image1)
        self.set_element_text('feature_image2', text=fea_image2)
        return True

    def get_terrain_offset_files(self):
        """
        get file paths of terrain offset
        Returns:(terrain offset 1,terrain offset 2, terrain offset 3, terrain offset 4)

        """
        ds1 = self.get_element_text('dem1_img1_ds1')
        ds2 = self.get_element_text('dem1_img2_ds2')
        ds3 = self.get_element_text('dem2_img1_ds3')
        ds4 = self.get_element_text('dem2_img2_ds4')
        if len(ds1) == 1 and len(ds2) == 1 and len(ds3) == 1 and len(ds4) == 1:
            return ds1[0], ds2[0], ds3[0], ds4[0]
        else:
            basic.outputlogMessage('the count of terrain offset is not 1')
            return  '', '', '', ''


    def set_terrain_offset_files(self,ds1,ds2,ds3,ds4):
        """
        set file paths of terrain offset
        Args:
            ds1:the path of terrain offset1
            ds2:the path of terrain offset2
            ds3:the path of terrain offset3
            ds4:the path of terrain offset4

        Returns:True if successful, False Otherwise

        """
        self.set_element_text('dem1_img1_ds1', text=ds1)
        self.set_element_text('dem1_img2_ds2', text=ds2)
        self.set_element_text('dem2_img1_ds3', text=ds3)
        self.set_element_text('dem2_img2_ds4', text=ds4)
        return True

    def set_base_offset_info(self,pair_id,work_dir,source_images_dir,saved_dir,image_path1,image_path2,b_keep_mid_file):
        self.set_element_text('pair_id',text=str(pair_id))
        self.set_element_text('work_dir', text=str(work_dir))
        self.set_element_text('saved_dir', text=str(saved_dir))
        self.set_element_text('source_images_dir', text=str(source_images_dir))
        self.set_element_text('source_image_1', text=str(image_path1))
        self.set_element_text('source_image_2', text=str(image_path2))
        self.set_element_text('keep_mid_file', text=str(b_keep_mid_file))


    def add_coregistration_info(self,tag,value_str,attrib=None):
        """
        add information in coregistration group
        Args:
            tag:tag name
            value_str:information value
            attrib:information attribute

        Returns:True if successful, assert if Otherwise

        """
        return self.add_element('coregistration',tag,text=value_str,attrib=attrib)


    def add_terrain_offset_info(self, tag, value_str, attrib=None):
        """
        add information in terrain offset group
        Args:
            tag:tag name
            value_str:information value
            attrib:information attribute

        Returns:True if successful, assert if Otherwise

        """
        return self.add_element('terrain_offset', tag, text=value_str, attrib=attrib)

    def add_subset_info(self,tag, value_str, attrib=None):
        """
        add information in subset group
        Args:
            tag:tag name
            value_str:information value
            attrib:information attribute

        Returns:True if successful, assert if Otherwise

        """
        return self.add_element('subset', tag, text=value_str, attrib=attrib)

    def set_offset_tracking_info(self,tag, value_str, attrib=None):
        self.set_sub_element('feature_tracking',tag,text=str(value_str))

    def add_offset_tracking_info(self,tag, value_str, attrib=None):
        self.add_element('feature_tracking',tag,text=str(value_str))

    def get_offset_tracking_info(self,tag):
        info_list = self.get_sub_element_text_with_p_tag('feature_tracking',tag)
        if len(info_list) == 1:
            return info_list[0]
        if len(info_list) == 0:
            return ''
        else:
            basic.outputlogMessage('waring: the count of %s is more than 1')
            return info_list[0]


def test():
    if len(sys.argv) < 2:
        return False
    xml_file = sys.argv[1]
    pre_meta_obj = ImgProMetaDataClass(xml_file)

    basic.outputlogMessage('end test')


if __name__=='__main__':
    test()
    pass