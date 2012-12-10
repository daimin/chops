package com.belstar.printerstat.util;

import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.ArrayList;
import java.util.List;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;
import org.xmlpull.v1.XmlPullParserFactory;
import org.xmlpull.v1.XmlSerializer;

import com.belstar.printerstat.entry.SendData;

import android.util.Log;

public class XmlGeter {
	


	private List<String> printerIDs = null;
	private List<String> customNames = null;
	private List<String> adminNames = null;
	private List<String> archivesTypes = null;
	
	public XmlGeter(String xmlText){
		parse(xmlText);
	}

	private void parse(String xmlText) {
		if (null == xmlText || xmlText.trim().length() <= 0) {
			return;
		}
		List <String>curList = null;
		xmlText = xmlText.trim();
		XmlPullParserFactory factory;
		try {
			factory = XmlPullParserFactory.newInstance();

			factory.setNamespaceAware(true);
			XmlPullParser parser = factory.newPullParser();
			parser.setInput(new StringReader(xmlText));

			int eventType = parser.getEventType();
			while (eventType != XmlPullParser.END_DOCUMENT) {
				switch (eventType) {
				case XmlPullParser.START_DOCUMENT:

					break;
				case XmlPullParser.START_TAG:
					if (parser.getName().equals("items")) {
						if(parser.getAttributeValue(0).equals("printer")){
							printerIDs = new ArrayList<String>();
							curList = printerIDs;
						}else if(parser.getAttributeValue(0).equals("custom")){
							customNames = new ArrayList<String>();
							curList = customNames;
						}else if(parser.getAttributeValue(0).equals("archives_type")){
							archivesTypes = new ArrayList<String>();
							curList = archivesTypes;
						}else if(parser.getAttributeValue(0).equals("admin")){
							adminNames = new ArrayList<String>();
							curList = adminNames;
						}
					}
					
					if(parser.getName().equals("item")){
						if(null != curList){
							curList.add(parser.nextText());
						}
						
					}

					break;
				case XmlPullParser.TEXT:
					break;
				case XmlPullParser.END_TAG:
					if(parser.getName().equals("items")){
						curList = null;
					}
					break;
				case XmlPullParser.END_DOCUMENT:
					break;
				}

				eventType = parser.next();
			}
		} catch (XmlPullParserException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public List<String> getPrinterIDs() {
		return printerIDs;
	}

	public List<String> getCustomNames() {
		return customNames;
	}

	public List<String> getAdminNames() {
		return adminNames;
	}

	public List<String> getArchivesTypes() {
		return archivesTypes;
	}
	
	
	public static String getSendDataXml(SendData sendData){
		StringWriter stringWriter = new StringWriter();  

        try {  
            // 获取XmlSerializer对象  
            XmlPullParserFactory factory = XmlPullParserFactory.newInstance();  
            XmlSerializer xmlSerializer = factory.newSerializer();  
            // 设置输出流对象  
            xmlSerializer.setOutput(stringWriter);  
            /* 
             * startDocument(String encoding, Boolean standalone)encoding代表编码方式 
             * standalone  用来表示该文件是否呼叫其它外部的文件。 
             * 若值是 ”yes” 表示没有呼叫外部规则文件，若值是 ”no” 则表示有呼叫外部规则文件。默认值是 “yes”。 
             */  
            xmlSerializer.startDocument("utf-8", true);  
            xmlSerializer.startTag(null, "Data");  
            xmlSerializer.startTag(null, "Send");
            
            xmlSerializer.startTag(null, "AdminName");
            xmlSerializer.text(sendData.getAdminName());
            xmlSerializer.endTag(null, "AdminName");
            
            xmlSerializer.startTag(null, "ArchivesType");
            xmlSerializer.text(sendData.getArchivesType());
            xmlSerializer.endTag(null, "ArchivesType");
            
            xmlSerializer.startTag(null, "CustomName");
            xmlSerializer.text(sendData.getCustomName());
            xmlSerializer.endTag(null, "CustomName");
            
            xmlSerializer.startTag(null, "Memo");
            xmlSerializer.text(sendData.getMemo());
            xmlSerializer.endTag(null, "Memo");
            
            xmlSerializer.startTag(null, "OverTime");
            xmlSerializer.text(sendData.getOverTime());
            xmlSerializer.endTag(null, "OverTime");
            
            xmlSerializer.startTag(null, "PostTime");
            xmlSerializer.text(sendData.getPostTime());
            xmlSerializer.endTag(null, "PostTime");
            
            xmlSerializer.startTag(null, "PrinterID");
            xmlSerializer.text(sendData.getPrinterID());
            xmlSerializer.endTag(null, "PrinterID");
            
            xmlSerializer.startTag(null, "SendTime");
            xmlSerializer.text(sendData.getSendTime());
            xmlSerializer.endTag(null, "SendTime");
            
            xmlSerializer.startTag(null, "ArchivesNum");
            xmlSerializer.text(sendData.getArchivesNum()+"");
            xmlSerializer.endTag(null, "ArchivesNum");
            
            xmlSerializer.startTag(null, "CounterInit");
            xmlSerializer.text(sendData.getCounterInit() + "");
            xmlSerializer.endTag(null, "CounterInit");
            
            xmlSerializer.startTag(null, "CounterOver");
            xmlSerializer.text(sendData.getCounterOver() + "");
            xmlSerializer.endTag(null, "CounterOver");
            
            xmlSerializer.startTag(null, "PaperScrap");
            xmlSerializer.text(sendData.getPaperScrap() + "");
            xmlSerializer.endTag(null, "PaperScrap");
            
            xmlSerializer.endTag(null, "Send");  
            xmlSerializer.endTag(null, "Data"); 
            xmlSerializer.endDocument();  
            
      
        } catch (Exception e) {  
            e.printStackTrace();  
        }  
        return stringWriter.toString();  

	}
	

}
