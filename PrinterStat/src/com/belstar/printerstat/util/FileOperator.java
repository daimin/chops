package com.belstar.printerstat.util;

import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import com.belstar.printerstat.Config;

import android.content.Context;

public class FileOperator {

	public static FileOutputStream openFileOutput(Context ctx,String gameFile, int i) throws FileNotFoundException {
		FileOutputStream fos = null;
		fos = ctx.openFileOutput(gameFile, i);
		return fos;
	}
	
	public static FileOutputStream openFileOutput(Context ctx,String filename) throws FileNotFoundException{
		return openFileOutput(ctx,filename,Context.MODE_PRIVATE);
		
	}
	
	public static FileInputStream openFileInput(Context ctx,String gameFile) throws FileNotFoundException {
        return ctx.openFileInput(gameFile);
	}
	
	public static void writeXMlDataFile(Context ctx, String xmlData){
		FileOutputStream xmlFile = null;
		try {
			xmlFile = openFileOutput(ctx, Config.XML_DATA_FILE);
			xmlFile.write(xmlData.getBytes());
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}finally{
			if(xmlFile != null){
				try {
					xmlFile.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
				xmlFile = null;
			}
		}
	}
	
	public static String readXmlDataFile(Context ctx){
		String res = "";
		FileInputStream xmlFile = null;
		ByteArrayOutputStream outStream = null;
		try {
			xmlFile = openFileInput(ctx, Config.XML_DATA_FILE);
			outStream = new ByteArrayOutputStream();
	        byte[] buffer=new byte[1024];

	        int len=0;
	        while ((len = xmlFile.read(buffer))!=-1){
	            outStream.write(buffer, 0, len);
	        }
	        res = new String(outStream.toByteArray());
		} catch (FileNotFoundException e) {
			
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}finally{
			if(xmlFile != null){
				try {
					xmlFile.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
				xmlFile = null;
			}
		}
		return res;
	}
}
