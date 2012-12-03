package com.belstar.printerstat.util;

import java.text.SimpleDateFormat;
import java.util.Date;

public class ComUtil {
	
	public static final String DATETIME_PATTERN = "yyyy-MM-dd HH:mm:ss";
	
	private static boolean isNull(String txt){
		if(null == txt || txt.trim().equals("")){
			return true;
		}
		return false;
	}
	
	
	public static String getTime(){
		SimpleDateFormat sdf = new SimpleDateFormat(DATETIME_PATTERN);
		return sdf.format(new Date());
	}
}
