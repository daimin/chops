package com.belstar.printerstat.util;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ComUtil {
	
	public static final String DATETIME_PATTERN = "yyyy-MM-dd HH:mm:ss";
	public static final String TIME_PATTERN = "HH:mm";
	
	private static boolean isNull(String txt){
		if(null == txt || txt.trim().equals("")){
			return true;
		}
		return false;
	}
	
	
	public static String getDateTime(){
		SimpleDateFormat sdf = new SimpleDateFormat(DATETIME_PATTERN);
		return sdf.format(new Date());
	}
	
	public static String getTime(){
		SimpleDateFormat sdf = new SimpleDateFormat(TIME_PATTERN);
		return sdf.format(new Date());
	}
	
	public static Date parseTime(String time){
		SimpleDateFormat sdf = new SimpleDateFormat(TIME_PATTERN);
		try {
			return sdf.parse(time);
		} catch (ParseException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	public static String getTimeByHourMin(int hours, int mins){
		String time = "";
		if(hours < 10){
			time = "0" + hours;
		}else{
			time = "" + hours;
		}
		if(mins < 10){
			time += ":0" + mins;
		}else{
			time += ":" + mins;
		}
		
		return time;
	}
}
