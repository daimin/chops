package com.belstar.printerstat.util;

public class ComUtil {
	
	private static boolean isNull(String txt){
		if(null == txt || txt.trim().equals("")){
			return true;
		}
		return false;
	}
}
