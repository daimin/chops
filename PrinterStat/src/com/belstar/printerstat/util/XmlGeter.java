package com.belstar.printerstat.util;

import java.io.IOException;
import java.io.StringReader;
import java.util.List;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;
import org.xmlpull.v1.XmlPullParserFactory;

public class XmlGeter {
	
	private String xmlText = "";
	
	private List<String> printerIDs = null;
	private List<String> customNames = null;
	private List<String> adminNames = null;
	private List<String> archivesTypes = null;
	
	public XmlGeter(String xmlText){
		this.xmlText = xmlText;
		parse(xmlText);
	}

	private void parse(String xmlText) {
		if (null == xmlText || xmlText.trim().length() <= 0) {
			
			return;
		}
		
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
					if (parser.getName().equals("err")) {
						
					}

					break;
				case XmlPullParser.TEXT:
					break;
				case XmlPullParser.END_TAG:
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
	
	

}
