package com.belstar.printerstat;

public interface Config {

	public static final String HOST = "http://192.168.211.91:13456";
	public static final String PUT_URL = HOST + "/put_data"; 
    public static final String GET_URL = HOST;
	//public static final String GET_URL = "http://192.168.0.120:13456";
	
	public static final String GET_DATA_KEY = "xml_data";
	
	
	public static final String NO_NET_CONN_KEY = "no_net_conn";
	
	public static final String TIMEOUT_KEY = "conn_time_out";
	
	public static final int LOADING_TIMEOUT = 2000;
	
	public static final String XML_DATA_FILE = "belstar.data";
	
	
}
