package com.belstar.printerstat;

public interface Config {

	public static final String PUT_URL = "http://192.168.1.103/PrinterStat/put_data.php"; 
	public static final String GET_URL = "http://192.168.211.91:13456";
//	public static final String GET_URL = "http://192.168.0.120:13456";
	
	public static final String GET_DATA_KEY = "xml_data";
	
	public static final int LOADING_TIMEOUT = 100;
	
	
}
