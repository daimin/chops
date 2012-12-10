package com.belstar.printerstat.entry;

public class SendData {
	private String printerID;
	private String customName;
	private String adminName;
	private String archivesType;
	private String postTime;
	private String overTime;
	private int archivesNum;
	private int counterInit;
	private int counterOver;
	private int paperScrap;
	private String memo;
	private String sendTime;

	public String getPrinterID() {
		return printerID;
	}

	public void setPrinterID(String printerID) {
		this.printerID = printerID;
	}

	public String getCustomName() {
		return customName;
	}

	public void setCustomName(String customName) {
		this.customName = customName;
	}

	public String getAdminName() {
		return adminName;
	}

	public void setAdminName(String adminName) {
		this.adminName = adminName;
	}

	public String getArchivesType() {
		return archivesType;
	}

	public void setArchivesType(String archivesType) {
		this.archivesType = archivesType;
	}

	public String getPostTime() {
		return postTime;
	}

	public void setPostTime(String postTime) {
		this.postTime = postTime;
	}

	public String getOverTime() {
		return overTime;
	}

	public void setOverTime(String overTime) {
		this.overTime = overTime;
	}

	public int getArchivesNum() {
		return archivesNum;
	}

	public void setArchivesNum(int archivesNum) {
		this.archivesNum = archivesNum;
	}

	public int getCounterInit() {
		return counterInit;
	}

	public void setCounterInit(int counterInit) {
		this.counterInit = counterInit;
	}

	public int getCounterOver() {
		return counterOver;
	}

	public void setCounterOver(int counterOver) {
		this.counterOver = counterOver;
	}

	public int getPaperScrap() {
		return paperScrap;
	}

	public void setPaperScrap(int paperScrap) {
		this.paperScrap = paperScrap;
	}

	public String getMemo() {
		return memo;
	}

	public void setMemo(String memo) {
		this.memo = memo;
	}

	public String getSendTime() {
		return sendTime;
	}

	public void setSendTime(String sendTime) {
		this.sendTime = sendTime;
	}

}
