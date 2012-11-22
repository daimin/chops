package com.belstar.printerstat.util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.impl.client.DefaultHttpClient;

public class NetUtil {

	/**
	 * 得到服务器响应的返回的字符串
	 * 
	 * @param response
	 * @return
	 */
	public static String GetStringEntity(HttpResponse response) {
		if (response == null) {
			return null;
		}
		HttpEntity entity = response.getEntity();
		if (entity != null)
			try {
				return StreamToString(entity.getContent());
			} catch (IllegalStateException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		return null;
	}
	
	/**
	 * 读取输入流中传入的字符串
	 * 
	 * @param is
	 * @return 字符串，如果读取失败返回null
	 */
	public static String StreamToString(InputStream is) {
		BufferedReader reader = new BufferedReader(new InputStreamReader(is));
		String ret = "";
		String line;
		try {
			while ((line = reader.readLine()) != null) {
				ret += line;
			}
			return ret;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	
	public static HttpResponse MakeRequest(HttpUriRequest areq) {
		DefaultHttpClient HttpManager = new DefaultHttpClient();
		try {
			final HttpResponse response = HttpManager.execute(areq);
			return response;
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {

			e.printStackTrace();
		}
		return null;

	}
	
	/**
	 * 得到服务器响应的返回的输入流
	 * 
	 * @param response
	 * @return
	 */
	public static InputStream GetInputStreamEntity(HttpResponse response) {
		if (response == null) {
			return null;
		}
		HttpEntity entity = response.getEntity();
		if (entity != null)
			try {
				return entity.getContent();
			} catch (IllegalStateException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		return null;
	}
}
