package com.belstar.printerstat;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.LinearLayout;

public class StatSelView extends LinearLayout {
	
	private LayoutInflater mInflater = null;
	private View sel_item;
	
	public StatSelView(Context context) {
		super(context);
		
		mInflater = LayoutInflater.from(context);
		sel_item = mInflater.inflate(R.layout.sel_item, null);
		this.addView(sel_item);
		
		
		
	}

}
