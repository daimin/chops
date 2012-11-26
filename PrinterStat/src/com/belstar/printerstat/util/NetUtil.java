package com.belstar.printerstat.util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.conn.ConnectTimeoutException;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpConnectionParams;

import com.belstar.printerstat.Config;

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

	public static HttpResponse MakeRequest(HttpUriRequest areq) throws ConnectTimeoutException {
		BasicHttpParams httpParameters = new BasicHttpParams();// Set the
																// timeout in
																// milliseconds
																// until a
																// connection is
																// established.
		HttpConnectionParams.setConnectionTimeout(httpParameters,
				Config.LOADING_TIMEOUT);
		// Set the default socket timeout (SO_TIMEOUT) // in milliseconds which
		// is the timeout for waiting for data.
		HttpConnectionParams.setSoTimeout(httpParameters,
				Config.LOADING_TIMEOUT);
		DefaultHttpClient HttpManager = new DefaultHttpClient(httpParameters);

		
		HttpResponse response = null;
		try {
			response = HttpManager.execute(areq);
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return response;

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
