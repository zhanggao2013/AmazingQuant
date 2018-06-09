#pragma warning (disable :4786)

#include "DFITCSECTraderApi.h"
#include "DFITCSECMdApi.h"
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
//#include "stdarg.h"
#include <cctype>
#include <string>
#include <cstring>
#include <string.h>
#include <vector>
#include <iostream>
#include <algorithm>
#include <iostream>
#include <sstream>
#include <unistd.h>
#include <map>
#include <pthread.h>
#if 0
#define __TRADE_TYPE__ DFITC_OPT_TYPE
#else
#define __TRADE_TYPE__ DFITC_COMM_TYPE
#endif//1

//�����б�
std::string func_index;
#pragma comment(lib, "DFITCMdApi.lib")

std::map<long,long> g_cccxMap;
std::map<long,long> g_ccmxMap;
std::map<long,long> g_wtMap;
std::map<long,long> g_cjMap;

namespace GTM
{
	long req_id		= 0;
	long local_id	= 1;
}
/*
static bool readMdgeFile(const char *filepath)
{
	bool rv;
	readConfCls readC(g_mp, "./log/readConfLogFolder/readConfLog.log");
	rv = readC.readFile(filepath, false);
	if (!rv)  return false;

	g_accountInfo.tfAddr         = readC.getString("mt", "tfAddr");//TradeFrontAddr.
	g_accountInfo.mfAddr         = readC.getString("mt", "mfAddr");//MdFrontAddr.
	g_accountInfo.sopAccountID   = readC.getString("mt", "SOPaccountID");
	g_accountInfo.sopPassword    = readC.getString("mt", "SOPpassWord");
	g_accountInfo.stockAccountID = readC.getString("mt", "stockAccountID");
	g_accountInfo.stockPassword  = readC.getString("mt", "stockPassWord");
	rv = readC.getBool("category", "stock",     g_category.m_stock);
	rv = readC.getBool("category", "sop",       g_category.m_sop);
	return true;
}

bool readConf()
{
	if (readMdgeFile("conf/mdgw.conf") == false)
		return false;
	return true;
}
*/
class CFunc
{
public:
	CFunc() : table_len(78)
	{
	}
public:
	bool ListInput(int key, std::string &value)
	{
		return input(key, value, m_input_list);
	}
	bool FieldInput(int key, std::string &value)
	{
		return input(key, value, m_field_list);
	}
	virtual void func_list_init()=0;
	void __continue()
	{
		std::string msg = "继续请输入Y";
		ShowInfo(msg);
		std::cin >> msg;
	}

protected:
	bool input(int key, std::string &value, const std::vector<std::string> &list)
	{
		if ((key > -1) && (key < list.size())) {
			std::string msg = list[key];
			ShowInfo(msg);
			std::cin >> value;
			return true;
		}
		return false;
	}
	void GetEnterLine(const std::string &hint, std::vector<std::string> &line_vec)
	{
		char * pstr_line = new char [hint.size()+1];
		strcpy(pstr_line, hint.c_str());
		char *line_p = pstr_line, * pos_1 = 0;
		while (true) {
			pos_1 = strstr(line_p, "\n");
			if (pos_1) {
				*pos_1 = '\0';
				line_vec.push_back(std::string(line_p));
				line_p = ++pos_1;
			} else if (line_p) {
				if ('\0' != line_p) {
					line_vec.push_back(std::string(line_p));
				}
				break;
			}
		}
		delete[] pstr_line;
	}
	void DrawTable(std::ostringstream &input, const std::vector<std::string> &line_vec)
	{
		std::string h;
		int line_vec_len = line_vec.size();

		for (int m = 0; m<line_vec_len; m++) {
			h = line_vec[m];
			while (true) {
				std::string s = "| " + h;
				int s_len = s.size();
				if (s_len > table_len-2) {
					std::string t = s.substr(0, table_len - 2);
					input << t << " |\n";
					h = s.substr(table_len - 2, s_len - table_len - 2);
				} else {
					std::string space_1;
					int space_len = table_len - s_len -2;
					for (int i=0; i<space_len; i++)	{
						space_1 += " ";
					}
					input << s << space_1 << " |\n";
					break;
				}
			}
		}
	}
	std::string GetTableLine()
	{
		std::string table_line;
		for (int i=0; i<table_len; i++)	{
			if ((0 == i) || (table_len-1 == i))
				table_line += "+";
			else
				table_line += "-";
		}
		return table_line;
	}
	void ShowInfo(const std::string &hint)
	{
		std::ostringstream input;
		std::vector<std::string> line_vec;
		std::string table_line = GetTableLine();
		GetEnterLine(hint, line_vec);
		input << table_line << "\n";
		DrawTable(input, line_vec);
		input << table_line << "\n";
		std::cout << std::string(input.str());
	}
public:
	std::vector<std::string> m_input_list;
	std::vector<std::string> m_field_list;
	const int table_len;
};


class CMdInput :public CFunc
{
public:
	CMdInput()
	{
		func_list_init();
	}
public:
	enum
	{
		_list = 0x00,	//功能列表
		_stocklogin,			//用户登录
		_stocklogout,		//用户登出
		_stocksubmardata,	//行情订阅
		_stockunsubmardata,  //取消行情订阅
		_soplogin,			//用户登录
		_soplogout,		//用户登出
		_sopsubmardata,	//行情订阅
		_sopunsubmardata,  //取消行情订阅
		_hqexit			//退出程序

	};
	enum
	{
		_host = 0x00,
			_acco_id,
			_pwd,
			_ppInstrumentID0,
			_ppInstrumentID1,
			_ppInstrumentID2
	};
public:
	void func_usage(DFITCSECMdApi &api)
	{
		std::string acco_id;
		std::string ppInstrumentID[3];
		char* contracts[3]={"","",""};
		const bool only = true;

		while (true)
		{

			if (ListInput(_list, func_index))
			{
				std::string pwd;

				switch (atoi(func_index.c_str()))
				{
				case _stocklogin:	//用户登录
					printf("A股用户登录\n");
					FieldInput(_acco_id,			acco_id);
					FieldInput(_pwd,				pwd);
					struct DFITCSECReqUserLoginField data;
					memset(&data,0,sizeof(data));
					strcpy(data.accountID,acco_id.c_str());
					strcpy(data.password, pwd.c_str());
					data.requestID=GTM::req_id++;
					api.ReqStockUserLogin(&data);
					break;
				case _stocklogout:	//用户登出
					printf("用户登出\n");
					if (!only)
						FieldInput(_acco_id,			acco_id);
					struct DFITCSECReqUserLogoutField data2;
					memset(&data2,0,sizeof(data2));
					strcpy(data2.accountID,acco_id.c_str());
					data2.requestID=GTM::req_id++;
					api.ReqStockUserLogout(&data2);
					break;
				case _stocksubmardata:
					printf("行情订阅\n");
					FieldInput(_ppInstrumentID0,			ppInstrumentID[0]);
					contracts[0]=(char*)ppInstrumentID[0].c_str();
					api.SubscribeStockMarketData(contracts, 1,GTM::req_id++);
					break;
				case _stockunsubmardata:
					printf("取消行情订阅\n");

					FieldInput(_ppInstrumentID0,			ppInstrumentID[0]);
					//FieldInput(_ppInstrumentID1,			ppInstrumentID[1]);
					//FieldInput(_ppInstrumentID2,			ppInstrumentID[2]);
					contracts[0]=(char*)ppInstrumentID[0].c_str();
					//contracts[1]=(char*)ppInstrumentID[1].c_str();
					//contracts[2]=(char*)ppInstrumentID[2].c_str();
					api.UnSubscribeStockMarketData(contracts,1,GTM::req_id++);
					break;
				case _soplogin:	//用户登录
					printf("期权用户登录\n");
					FieldInput(_acco_id,			acco_id);
					FieldInput(_pwd,				pwd);
					struct DFITCSECReqUserLoginField data3;
					memset(&data3,0,sizeof(data3));
					strcpy(data3.accountID,acco_id.c_str());
					strcpy(data3.password, pwd.c_str());
					data3.requestID=GTM::req_id++;
					api.ReqSOPUserLogin(&data3);
					break;
				case _soplogout:	//用户登出
					printf("用户登出\n");
					if (!only)
						FieldInput(_acco_id,			acco_id);
					struct DFITCSECReqUserLogoutField data4;
					memset(&data4,0,sizeof(data4));
					strcpy(data4.accountID,acco_id.c_str());
					data4.requestID=GTM::req_id++;
					api.ReqSOPUserLogout(&data4);
					break;
				case _sopsubmardata:
					printf("行情订阅\n");
					FieldInput(_ppInstrumentID0,			ppInstrumentID[0]);
					contracts[0]=(char*)ppInstrumentID[0].c_str();
					api.SubscribeSOPMarketData(contracts, 1,GTM::req_id++);
					break;
				case _sopunsubmardata:
					printf("取消行情订阅\n");

					FieldInput(_ppInstrumentID0,			ppInstrumentID[0]);
					contracts[0]=(char*)ppInstrumentID[0].c_str();
					api.UnSubscribeSOPMarketData(contracts,1,GTM::req_id++);
					break;
				case _hqexit:		//退出程序
					printf("退出行情连接成功\n");
					return;
				default:
					printf("请重新输入选项\n");
					break;
				}
			}
			__continue();
			//printf("rsp %s\n", GTM::rsp_msg);
			//memset(GTM::rsp_msg, 0, sizeof(GTM::rsp_msg));
		}
	}

private:
	void func_list_init()
	{
		char func_id_list[1024] = {0};
		sprintf(func_id_list,\
			"%d.stock用户登录%d.stock用户登出%d.stock行情订阅\n"\
			"%d.stock取消行情订阅%d.sop用户登录%d.sop用户登出\n"\
			"%d.sop行情订阅%d.sop取消行情订阅%d.退出行情连接",\
			_stocklogin, _stocklogout,_stocksubmardata,_stockunsubmardata,_soplogin, _soplogout,_sopsubmardata,_sopunsubmardata,_hqexit);
		m_input_list.push_back(std::string(func_id_list));
		m_field_list.push_back("输入行情前置机地址");	//_host
		m_field_list.push_back("输入资金账户");			//_acco_id
		m_field_list.push_back("输入登录密码");			//_pwd
		m_field_list.push_back("输入合约代码1");
		m_field_list.push_back("输入合约代码2");
		m_field_list.push_back("输入合约代码3");
	}
};


class CInput : public CFunc
{
public:
	CInput()
	{
		func_list_init();
	}
public:
	enum
	{
		_list = 0x00,	//功能列表
		_stocklogin,			//用户登录
		_stocklogout,		//用户登出
		_stockinsert,		//委托下单
		_stockcancel,		//委托撤单
		_stockwtcx,			//委托查询
		_stockcccx,			//持仓查询
		_soplogin,			//用户登录
		_soplogout,		//用户登出
		_sopinsert,		//委托下单
		_quitexit,			//退出程序
		_init           //初始化连接
	};
	enum
	{
		_host = 0x00,
			_stockacco_id,
			_stockpwd,
			_sopacco_id,
			_soppwd,
			_instrument_id,
			_price,
			_amount,
			_is_exchange_id,
			_is_instrument_id,
			_exchange_id,
			_local_id,
			_buy_sell,
			_newpwd,
			_date,
			_confirm_flag,
			_clientID,
			_clientID2,
			_closeAccount,
			_seatCode,
			_logical,
			_summaryWay,
			_filesFlag,
			_is_input,
			_insert_type,		//合约类型
			_quoteID,			//询价编号
			_openCloseFlag,
			_stayTime,
			_soporderType,	//sop订单类型
			_stockorderType,		//stock订单类型
			_entrustBatchID,		//委托批次号
			_eachSeatID,			//对方席位号
			_spdOrderID,				//柜台委托号
			_withdrawFlag,			//撤销标志
			_incQryIndex,			//增量查询索引值
			_entrustQryFlag,		//查询标志
			_coveredFlag,			//备兑类型
			_orderCategory,			//委托单类别
			_orderExpiryDate,		//订单时效限制
			_serialID,				//扩展流水号;

	};
public:
	void func_usage(DFITCSECTraderApi &api)
	{
		std::string stockacco_id;
		std::string sopacco_id;
		const bool only = true;

		while (true)
		{

			if (ListInput(_list, func_index))
			{
				std::string stockpwd;
				std::string soppwd;
				std::string newpwd;
				std::string clientid;
				std::string clientid2;
				std::string date;
				std::string confirm_flag;
				std::string close_account;
				std::string is_input;
				std::string seat_code;
				std::string logical;
				std::string summaryWay;
				std::string filesFlag;
				std::string instrument_id;
				std::string price;
				std::string amount;
				std::string price1;
				std::string amount2;
				std::string exchange_id;
				std::string is_instrument_id;
				std::string local_id;
				std::string buy_sell;
				std::string inserttype;
				std::string orderType;
				std::string entrustBatchID;
				std::string spdOrderID;
				std::string withdrawFlag;
				std::string incQryIndex;
				std::string entrustQryFlag;
				std::string openCloseFlag;
				std::string coveredFlag;
				std::string orderCategory;
				bool bsflag = false;

				//做市商专用
				std::string quoteID;                      //询价编号
				std::string bOrderAmount;                 //报单数量（买）
				std::string sOrderAmount;                 //报单数量（卖）
				std::string bInsertPrice;                 //委托价格（买）
				std::string sInsertPrice;                 //委托价格（卖）
				std::string bOpenCloseType;               //开平标志（买）
				std::string sOpenCloseType;               //开平标志（卖）
				std::string bSpeculator;                  //投资类别（买）
				std::string sSpeculator;                  //投资类别（卖）
				std::string stayTime;                     //停留时间，仅支持郑州。其它情况可设置为0

				switch (atoi(func_index.c_str()))
				{
				case _stocklogin:	//用户登录
					printf("stock用户登录\n");
					FieldInput(_stockacco_id,			stockacco_id);
					FieldInput(_stockpwd,				stockpwd);
					struct DFITCSECReqUserLoginField data;
					memset(&data,0,sizeof(data));
					strcpy(data.accountID,stockacco_id.c_str());
					strcpy(data.password, stockpwd.c_str());
					data.requestID=GTM::req_id++;
					api.ReqStockUserLogin(&data);
					break;
				case _stocklogout:	//用户登出
					printf("stock用户登出\n");
					if (!only)
						FieldInput(_stockacco_id,			stockacco_id);
					struct DFITCSECReqUserLogoutField data2;
					memset(&data2,0,sizeof(data2));
					strcpy(data2.accountID,stockacco_id.c_str());
					data2.requestID=GTM::req_id++;
					api.ReqStockUserLogout(&data2);
					break;
				case _stockinsert:	//委托下单
					printf("stock委托下单\n");
					if (!only)
						FieldInput(_stockacco_id,			stockacco_id);
					FieldInput(_instrument_id,		instrument_id);//合约代码
					FieldInput(_price,				price);//委托价格
					FieldInput(_buy_sell,			buy_sell);//委托类别
					FieldInput(_amount,				amount);//委托数量
					FieldInput(_stockorderType,				orderType);//订单类型
					//FieldInput(_entrustBatchID,				entrustBatchID);//委托批次号
					FieldInput(_exchange_id,		exchange_id);//交易所代码
					struct DFITCStockReqEntrustOrderField data3;
					memset(&data3,0,sizeof(data3));
					data3.entrustPrice = atof(price.c_str()); //报单价格
					data3.entrustDirection = atoi(buy_sell.c_str());//委托类别
					data3.entrustQty = atoi(amount.c_str());//下单数量
					data3.orderType = atoi(orderType.c_str()); //报单类型
					//data3.entrustBatchID = atoi(entrustBatchID.c_str());//委托批次号

					strcpy( data3.accountID,stockacco_id.c_str());//资金账户ID
					strcpy(data3.exchangeID,  exchange_id.c_str());//交易所代码
					strcpy( data3.securityID, instrument_id.c_str());//证券代码
					data3.localOrderID=GTM::local_id++;
					data3.requestID=GTM::req_id++;
					api.ReqStockEntrustOrder( &data3);
					break;
				case _stockcancel:	//委托撤单
					printf("stock撤单处理\n");
					if (!only)
					FieldInput(_stockacco_id,			stockacco_id);
					FieldInput(_local_id,			local_id);
					FieldInput(_spdOrderID,			spdOrderID);//柜台委托号
					struct DFITCSECReqWithdrawOrderField data4;
					memset(&data4,0,sizeof(data4));
					data4.requestID=GTM::req_id++;
					strcpy( data4.accountID,stockacco_id.c_str());//资金账户ID
					data4.localOrderID=atoi(local_id.c_str());
					api.ReqStockWithdrawOrder(&data4);
					break;
				case _stockwtcx:		//委托查询
					printf("stock委托查询\n");
					if (!only)
						FieldInput(_stockacco_id,			stockacco_id);
					FieldInput(_exchange_id,		exchange_id);//交易所代码
					FieldInput(_instrument_id,		instrument_id);//合约代码
					//FieldInput(_withdrawFlag,		withdrawFlag);//撤销标志
					//FieldInput(_incQryIndex,			incQryIndex);//增量查询索引值(N)
					FieldInput(_spdOrderID,			spdOrderID);//柜台委托号
					FieldInput(_buy_sell,			buy_sell);//委托类别
					//FieldInput(_entrustBatchID,				entrustBatchID);//委托批次号
					//FieldInput(_entrustQryFlag,				entrustQryFlag);//查询标志
					struct DFITCStockReqQryEntrustOrderField  data5;
					memset(&data5,0,sizeof(data5));
					data5.requestID=GTM::req_id++;
					strcpy(data5.exchangeID,  exchange_id.c_str());//交易所代码
					strcpy( data5.accountID,stockacco_id.c_str());//资金账户ID
					strcpy( data5.securityID, instrument_id.c_str());//证券代码
					//strcpy(data5.withdrawFlag, withdrawFlag.c_str());			//撤销标志(N)
					//strcpy(data.incQryIndex, this->m_sZLSYZ );			//增量查询索引值(N)
					data5.spdOrderID =  atoi(spdOrderID.c_str());			//柜台委托号(N)
					data5.entrustDirection =  atoi(buy_sell.c_str());			//委托类别(N)
					//data5.entrustBatchID =  atoi(entrustBatchID.c_str());			//委托批次号(N)
					//data5.entrustQryFlag =  atoi(entrustQryFlag.c_str());			//查询标志(N)
					api.ReqStockQryEntrustOrder(&data5);
					break;
				case _stockcccx:		//持仓查询
					printf("stock持仓查询\n");
					if (!only)
						FieldInput(_stockacco_id,			stockacco_id);
					FieldInput(_exchange_id,		exchange_id);//交易所代码
					FieldInput(_instrument_id,	instrument_id);
					FieldInput(_entrustQryFlag,				entrustQryFlag);//查询标志

					struct DFITCStockReqQryPositionField data6;
					memset(&data6,0,sizeof(data6));
					data6.requestID=GTM::req_id++;
					strcpy(data6.exchangeID,  exchange_id.c_str());//交易所代码
					strcpy( data6.accountID,stockacco_id.c_str());//资金账户ID
					strcpy( data6.securityID, instrument_id.c_str());//证券代码
					data6.posiQryFlag =  atoi(entrustQryFlag.c_str());			//查询标志(N)
					api.ReqStockQryPosition(&data6);
					break;
				case _soplogin:
					printf("用户登录\n");
					FieldInput(_sopacco_id,			sopacco_id);
					FieldInput(_soppwd,				soppwd);
					struct DFITCSECReqUserLoginField sopdata;
					memset(&sopdata,0,sizeof(data));
					strcpy(sopdata.accountID,sopacco_id.c_str());
					strcpy(sopdata.password, soppwd.c_str());
					sopdata.requestID=GTM::req_id++;
					api.ReqSOPUserLogin(&sopdata);
					break;
				case _soplogout:
					printf("用户登出\n");
					if (!only)
						FieldInput(_sopacco_id,			sopacco_id);
					struct DFITCSECReqUserLogoutField sopdata2;
					memset(&sopdata2,0,sizeof(data2));
					strcpy(sopdata2.accountID,sopacco_id.c_str());
					sopdata2.requestID=GTM::req_id++;
					api.ReqSOPUserLogout(&sopdata2);
					break;
				case _sopinsert:	//委托下单
					printf("委托下单\n");
					if (!only)
						FieldInput(_sopacco_id,			sopacco_id);
					FieldInput(_instrument_id,		instrument_id);//合约代码
					FieldInput(_exchange_id,		exchange_id);//交易所代码
					FieldInput(_buy_sell,			buy_sell);//委托类别
					FieldInput(_amount,				amount);//委托数量
					FieldInput(_price,				price);//委托价格
					FieldInput(_openCloseFlag,		openCloseFlag);//开平标志
					FieldInput(_coveredFlag,		coveredFlag);//备兑类型
					FieldInput(_orderCategory,				orderCategory);//委托单类别
					FieldInput(_soporderType,				orderType);///订单类型
					DFITCSOPReqEntrustOrderField sopdata3;
								memset(&sopdata3, 0, sizeof(sopdata3));
					strcpy(sopdata3.accountID,sopacco_id.c_str());//资金账户ID
					strcpy( sopdata3.securityID, instrument_id.c_str());//证券代码
					strcpy(sopdata3.exchangeID,  exchange_id.c_str());//交易所代码
					sopdata3.entrustDirection = atoi(buy_sell.c_str());//委托类别
					sopdata3.entrustQty = atoi(amount.c_str());//下单数量
					sopdata3.entrustPrice = atof(price.c_str()); //报单价格
					sopdata3.openCloseFlag = atoi(openCloseFlag.c_str());//开平标志
					sopdata3.coveredFlag = atoi(coveredFlag.c_str());//备兑类型
					sopdata3.orderCategory = atoi(coveredFlag.c_str());//委托单类别
					sopdata3.orderType = atoi(orderType.c_str()); //报单类型
					strcpy(sopdata3.accountID,sopacco_id.c_str());//资金账户ID


					sopdata3.localOrderID=GTM::local_id++;
					sopdata3.requestID=GTM::req_id++;
					api.ReqSOPEntrustOrder( &sopdata3);
					break;
				case _quitexit:		//退出程序
					printf("退出交易连接成功\n");
					return;
				default:
					printf("请重新输入选项\n");
					break;
				}
			}

			__continue();
			//printf("rsp %s\n", GTM::rsp_msg);
			//memset(GTM::rsp_msg, 0, sizeof(GTM::rsp_msg));
		}
	}


private:
	void func_list_init()
	{
		char func_id_list[1024] = {0};
		/*
		sprintf(func_id_list,\
			" %d.stock用户登录    %d.stock用户登出   %d.stock委托下单   %d.stock委托撤单\n"\
			" %d.stock委托查询    %d.stock持仓查询\n"\
			"%d.sop用户登录    %d.sop用户登出   %d.sop委托下单 %d.退出交易"\
			,_stocklogin, _stocklogout, _stockinsert,_stockcancel\
			,_stockwtcx,_stockcccx\
			,_soplogin, _soplogout, _sopinsert,_quitexit);*/
		sprintf(func_id_list,\
				"%d.stock用户登陆%d.stock用户登出%d.stock委托下单\n"\
				"%d.stock委托撤单%d.stock委托查询%d.stock持仓查询\n"\
				"%d.sop用户登陆%d.sop用户登出%d.sop委托下单%d.退出交易"\
				,_stocklogin, _stocklogout, _stockinsert,_stockcancel\
				,_stockwtcx,_stockcccx\
				,_soplogin, _soplogout, _sopinsert,_quitexit);
		m_input_list.push_back(std::string(func_id_list));

		m_field_list.push_back("输入交易前置机地址");		//_host
		m_field_list.push_back("输入stock资金账户");				//_acco_id
		m_field_list.push_back("输入stock登录密码");				//_pwd
		m_field_list.push_back("输入sop资金账户");				//_acco_id
		m_field_list.push_back("输入sop登录密码");				//_pwd
		m_field_list.push_back("输入合约代码");				//_instrument_id
		m_field_list.push_back("输入委托价格");				//_price
		m_field_list.push_back("输入委托数量");				//_amount
		m_field_list.push_back("是否输入交易所");			//_is_exchange_id
		m_field_list.push_back("是否输入合约代码");			//_is_instrument_id
		m_field_list.push_back("输入交易所");				//_exchange_id
		m_field_list.push_back("输入本地委托号");			//_local_id
		m_field_list.push_back("输入委托类别:(1(买),2(卖))");				//_buy_sell
		m_field_list.push_back("输入新密码");				//_newpw,
		m_field_list.push_back("输入日期(yyyy.mm.dd)");	//_begin_data,
		m_field_list.push_back("输入确认标志");				//_confirm_flag
		m_field_list.push_back("交易编码");					//_clientID
		m_field_list.push_back("交易编码2");				//_clientID2
		m_field_list.push_back("结算账户");					//_closeAccount
		m_field_list.push_back("席位代码");					//_seatCode
		m_field_list.push_back("是否进行逻辑判断");			//_logical
		m_field_list.push_back("汇总标志");					//_summaryWay
		m_field_list.push_back("档案类型");					//_filesFlag
		m_field_list.push_back("是否继续输入(y/n)");		//_is_input
		m_field_list.push_back("合约类型");
		m_field_list.push_back("询价编号");
		m_field_list.push_back("开平标志：1(开),2(平)");
		m_field_list.push_back("停留时间（仅支持郑州）");
		m_field_list.push_back("订单类型:1限价,2市价,3市价剩余转限价,4组合");//sop
		m_field_list.push_back("订单类型:");//stock
		m_field_list.push_back("委托批次号");
		m_field_list.push_back("对方席位号");
		m_field_list.push_back("柜台委托号");
		m_field_list.push_back("撤销标志");
		m_field_list.push_back("增量查询索引值");
		m_field_list.push_back("查询标志");
		m_field_list.push_back("备兑类型:0(非备兑),1(备兑),2(备兑优先)");
		//m_field_list.push_back("委托单类别:0(普通委托),1(手动强平单),2(行情触发),8(自动强平)");
		m_field_list.push_back("委托单类别:0普通,1手动强平,2行情触发,8自动强平");
		m_field_list.push_back("订单时效限制");
		m_field_list.push_back("扩展流水号");

	}

};



//行情响应类
class HQHandler:public DFITCSECMdSpi
{
public:
	virtual void OnFrontConnected()
	{
		char rsp_msg[4096] = {0};
		sprintf(rsp_msg, "行情前置机连接！");
		printf("%s\n",rsp_msg);
	}	
    virtual void OnFrontDisconnected( int nReason )
	{
    	char rsp_msg[4096] = {0};
		sprintf(rsp_msg, "行情前置机连接断开:%d",nReason);
		printf("%s\n",rsp_msg);
	}

    virtual void OnRspStockUserLogin(struct DFITCSECRspUserLoginField * pRspUserLogin, struct DFITCSECRspInfoField * pRspInfo)
	{
    	char rsp_msg[40960] = {0};
		if (pRspUserLogin)
		{
			sprintf(rsp_msg, "SEC-登录响应 : [请求ID]:[%ld],[客户号]:[%s],[会话编号]:[%ld],[前置编号]:[%ld],[本地委托号]:[%ld],[登录时间]:[%s],[交易日]:[%d],[结果]:[%ld],[返回信息]:[%s]",
					pRspUserLogin->requestID,//请求ID
					pRspUserLogin->accountID,//客户号
					pRspUserLogin->sessionID,//会话编号
					pRspUserLogin->frontID,//前置编号
					pRspUserLogin->localOrderID,//本地委托号
					pRspUserLogin->loginTime,//登录时间
					pRspUserLogin->tradingDay,//交易日
					pRspUserLogin->result,//结果
					"登陆成功");//返回信息
		}
		if (pRspInfo)
				{
					sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							pRspInfo->errorMsg);//错误信息
				}
		printf("%s\n",rsp_msg);
	}

    virtual void OnRspStockUserLogout(struct DFITCSECRspUserLogoutField * pRspUsrLogout, struct DFITCSECRspInfoField * pRspInfo)
	{
    	char rsp_msg[4096] = {0};
    	if (pRspUsrLogout)
    	{
    		sprintf(rsp_msg, "SEC-登出响应 : [请求ID]:[%ld],[客户号]:[%s],[结果]:[%ld],[返回信息]:[%s]",
    				pRspUsrLogout->requestID,//请求ID
					pRspUsrLogout->accountID,//客户号
					pRspUsrLogout->result,//结果
					"登出成功");//返回信息
    	}
    	if (pRspInfo)
    			{
    				sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
    						pRspInfo->requestID,//请求ID
    						pRspInfo->sessionID,//会话标识
    						pRspInfo->accountID,//客户号
    						pRspInfo->errorID,//错误ID
    						pRspInfo->localOrderID,//本地委托号
    						pRspInfo->spdOrderID,//柜台委托号
    						pRspInfo->errorMsg);//错误信息
    			}
    	printf("%s\n",rsp_msg);
	}
    //STOCK-可用行情响应
    virtual void OnRspStockAvailableQuot(struct DFITCRspQuotQryField * pAvailableQuotInfo, struct DFITCSECRspInfoField * pRspInfo,bool flag)
	{
    	char rsp_msg[4096] = {0};
    	if (pAvailableQuotInfo)
    	{
    		sprintf(rsp_msg,"-可用行情信息查询响应: [交易所]:[%s],[合约代码]:[%s]",
    				pAvailableQuotInfo->exchangeID,//交易所
					pAvailableQuotInfo->securityID);//合约名称
    	}
    	if (pRspInfo)
    			{
    				sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
    						pRspInfo->requestID,//请求ID
    						pRspInfo->sessionID,//会话标识
    						pRspInfo->accountID,//客户号
    						pRspInfo->errorID,//错误ID
    						pRspInfo->localOrderID,//本地委托号
    						pRspInfo->spdOrderID,//柜台委托号
    						pRspInfo->errorMsg);//错误信息
    			}
    	printf("%s\n",rsp_msg);
	}
    //STOCK-行情订阅响应
    virtual void OnRspStockSubMarketData(struct DFITCSECSpecificInstrumentField * pSpecificInstrument, struct DFITCSECRspInfoField * pRspInfo)
	{
    	char rsp_msg[4096] = {0};
    	if (pRspInfo)
    			{
    				sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
    						pRspInfo->requestID,//请求ID
    						pRspInfo->sessionID,//会话标识
    						pRspInfo->accountID,//客户号
    						pRspInfo->errorID,//错误ID
    						pRspInfo->localOrderID,//本地委托号
    						pRspInfo->spdOrderID,//柜台委托号
    						pRspInfo->errorMsg);//错误信息
    			}
    	if (pSpecificInstrument)
		{
    		sprintf(rsp_msg,"行情订阅响应: [请求ID]:[%ld],[合约代码]:[%s],[交易所代码]:[%s]",
    				pSpecificInstrument->requestID,//请求ID
					pSpecificInstrument->securityID,//合约代码
					pSpecificInstrument->exchangeID);//交易所代码
		}
    	printf("%s\n",rsp_msg);
		
	}
    //STOCK-取消订阅行情响应
    virtual void OnRspStockUnSubMarketData(struct DFITCSECSpecificInstrumentField * pSpecificInstrument, struct DFITCSECRspInfoField * pRspInfo)
	{
    	char rsp_msg[4096] = {0};
    	if (pRspInfo)
		{
			sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
					pRspInfo->requestID,//请求ID
					pRspInfo->sessionID,//会话标识
					pRspInfo->accountID,//客户号
					pRspInfo->errorID,//错误ID
					pRspInfo->localOrderID,//本地委托号
					pRspInfo->spdOrderID,//柜台委托号
					pRspInfo->errorMsg);//错误信息
		}
    	if (pSpecificInstrument)
		{
			sprintf(rsp_msg,  "行情退订响应: [请求ID]:[%ld],[合约代码]:[%s],[交易所代码]:[%s]",
					pSpecificInstrument->requestID,//请求ID
					pSpecificInstrument->securityID,//合约代码
					pSpecificInstrument->exchangeID);//交易所代码
		}
    	printf("%s\n",rsp_msg);
	}
    //stock-行情消息
    virtual void OnStockMarketData(struct DFITCStockDepthMarketDataField *pMarketDataField)
	{
    	char rsp_msg[4096] = {0};
		sprintf(rsp_msg, "股票行情更新：[证券代码]：[%s],[交易所]:[%s],[最新价]:[%.3f],[昨收盘]:[%.3f],[今开盘]:[%.3f],[涨停价]:[%.3f],[跌停价]:[%.3f],[时间戳]:[%s]",
				pMarketDataField->staticDataField.securityID,
				pMarketDataField->staticDataField.exchangeID,
				pMarketDataField->sharedDataField.latestPrice,
				pMarketDataField->staticDataField.preClosePrice,
				pMarketDataField->staticDataField.openPrice,
				pMarketDataField->staticDataField.upperLimitPrice,
				pMarketDataField->staticDataField.lowerLimitPrice,
				pMarketDataField->sharedDataField.updateTime);
		printf("%s\n",rsp_msg);
	}
    //sop-sop登录响应
    virtual void OnRspSOPUserLogin(struct DFITCSECRspUserLoginField * pRspUserLogin, struct DFITCSECRspInfoField * pRspInfo)
    {
    	char rsp_msg[4096] = {0};
    	if (pRspUserLogin)
    	{
    		sprintf(rsp_msg,"SEC-登录响应 : [请求ID]:[%ld],[客户号]:[%s],[会话编号]:[%ld],[前置编号]:[%ld],[本地委托号]:[%ld],[登录时间]:[%s],[交易日]:[%d],[结果]:[%ld],[返回信息]:[%s]",
    				pRspUserLogin->requestID,//请求ID
					pRspUserLogin->accountID,//客户号
					pRspUserLogin->sessionID,//会话编号
					pRspUserLogin->frontID,//前置编号
					pRspUserLogin->localOrderID,//本地委托号
					pRspUserLogin->loginTime,//登录时间
					pRspUserLogin->tradingDay,//交易日
					pRspUserLogin->result,//结果
    				"登录成功");//返回信息
    	}
    	if(pRspInfo)
    	{
    		sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
    									pRspInfo->requestID,//请求ID
    									pRspInfo->sessionID,//会话标识
    									pRspInfo->accountID,//客户号
    									pRspInfo->errorID,//错误ID
    									pRspInfo->localOrderID,//本地委托号
    									pRspInfo->spdOrderID,//柜台委托号
    									"登录失败");//错误信息
    	}
    	printf("%s\n",rsp_msg);
    }
    //sop登出响应
    virtual void OnRspSOPUserLogout(struct DFITCSECRspUserLogoutField * pRspUsrLogout, struct DFITCSECRspInfoField * pRspInfo)
    {
    	char rsp_msg[4096] = {0};
    	if(pRspUsrLogout)
    	{
    		sprintf(rsp_msg,"SEC-登出响应 : [请求ID]:[%ld],[客户号]:[%s],[结果]:[%ld],[返回信息]:[%s]",
    				pRspUsrLogout->requestID,//请求ID
					pRspUsrLogout->accountID,//客户号
					pRspUsrLogout->result,//结果
    				"登出成功");//返回信息
    	}
    	if(pRspInfo)
    	{
    		sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
					pRspInfo->requestID,//请求ID
					pRspInfo->sessionID,//会话标识
					pRspInfo->accountID,//客户号
					pRspInfo->errorID,//错误ID
					pRspInfo->localOrderID,//本地委托号
					pRspInfo->spdOrderID,//柜台委托号
					"登出失败");//错误信息
    	}
    	printf("%s\n",rsp_msg);
    }
    //sop行情订阅
    virtual void OnRspSOPSubMarketData(struct DFITCSECSpecificInstrumentField * pSpecificInstrument, struct DFITCSECRspInfoField * pRspInfo)
    {
    	char rsp_msg[4096] = {0};
    	if(pSpecificInstrument)
    	{
    		sprintf(rsp_msg,"行情订阅响应: [请求ID]:[%ld],[合约代码]:[%s],[交易所代码]:[%s]",
    				pSpecificInstrument->requestID,//请求ID
					pSpecificInstrument->securityID,//合约代码
					pSpecificInstrument->exchangeID);//交易所代码
    	}
    	if(pRspInfo)
    	{
    		sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
					pRspInfo->requestID,//请求ID
					pRspInfo->sessionID,//会话标识
					pRspInfo->accountID,//客户号
					pRspInfo->errorID,//错误ID
					pRspInfo->localOrderID,//本地委托号
					pRspInfo->spdOrderID,//柜台委托号
					"行情订阅失败");//错误信息
    	}
    	printf("%s\n",rsp_msg);
    }
    virtual void OnRspSOPUnSubMarketData(struct DFITCSECSpecificInstrumentField * pSpecificInstrument, struct DFITCSECRspInfoField * pRspInfo)
    {
    	char rsp_msg[4096] = {0};
    	if(pSpecificInstrument)
    	{
    		sprintf(rsp_msg,"行情退订响应: [请求ID]:[%ld],[合约代码]:[%s],[交易所代码]:[%s]",
    				pSpecificInstrument->requestID,//请求ID
					pSpecificInstrument->securityID,//合约代码
					pSpecificInstrument->exchangeID);//交易所代码
    	}
    	if(pRspInfo)
    	{
    		sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
					pRspInfo->requestID,//请求ID
					pRspInfo->sessionID,//会话标识
					pRspInfo->accountID,//客户号
					pRspInfo->errorID,//错误ID
					pRspInfo->localOrderID,//本地委托号
					pRspInfo->spdOrderID,//柜台委托号
					"行情退订失败");//错误信息
    	}
    	printf("%s\n",rsp_msg);
    }
    virtual void OnSOPMarketData(struct DFITCSOPDepthMarketDataField *pMarketDataField)
    {
    	char rsp_msg[4096] = {0};
    	sprintf(rsp_msg,"股票行情更新：[合约代码]:[%s],[交易所]:[%s],[期权标识代码]:[%s],[最新价]:[%.4f],[昨收盘价]:[%.4f],[开盘价]:[%.4f],[涨停价]:[%.4f],[跌停价]:[%.4f],[时间戳]:[%s]",
    			pMarketDataField->staticDataField.securityID,
				pMarketDataField->staticDataField.exchangeID,
				pMarketDataField->specificDataField.contractID,
				pMarketDataField->sharedDataField.latestPrice,
				pMarketDataField->staticDataField.preClosePrice,
				pMarketDataField->staticDataField.openPrice,
				pMarketDataField->staticDataField.upperLimitPrice,
				pMarketDataField->staticDataField.lowerLimitPrice,
				pMarketDataField->sharedDataField.updateTime);
    	printf("%s\n",rsp_msg);
    }
};





//交易响应类
class JYHandler:public DFITCSECTraderSpi
{
public:
	//前置连接
	virtual void OnFrontConnected()
	{
		printf("交易前置连接！");
	}
	//前置连接断开
	virtual void OnFrontDisconnected( int nReason )
	{
		printf( "交易前置断开连接:%d",nReason);
	}
	//错误应答
	virtual void OnRspError(DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		sprintf(rsp_msg,"[请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
																													pRspInfo->requestID,			//请求ID
																													pRspInfo->sessionID,			//会话标识
																													pRspInfo->accountID,			//客户号
																													pRspInfo->errorID,			//错误ID
																													pRspInfo->localOrderID,			//本地委托号
																													pRspInfo->spdOrderID,			//柜台委托号
																													pRspInfo->errorMsg);
		printf("%s\n",rsp_msg);
	}
	//stock-登陆响应
	virtual void OnRspStockUserLogin(DFITCSECRspUserLoginField *pRspUserLogin, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		if ( pRspUserLogin)
		{
			sprintf(rsp_msg, "SEC-登录响应 : [请求ID]:[%ld],[客户号]:[%s],[会话编号]:[%ld],[前置编号]:[%ld],[本地委托号]:[%ld],[登录时间]:[%s],[交易日]:[%d],[结果]:[%ld],[返回信息]:[%s]",
					pRspUserLogin->requestID,//请求ID
					pRspUserLogin->accountID,//客户号
					pRspUserLogin->sessionID,//会话编号
					pRspUserLogin->frontID,//前置编号
					pRspUserLogin->localOrderID,//本地委托号
					pRspUserLogin->loginTime,//登录时间
					pRspUserLogin->tradingDay,//交易日
					pRspUserLogin->result,//结果
					"登陆成功");//返回信息
		}
		if ( pRspInfo)
		{

			sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
					pRspInfo->requestID,//请求ID
					pRspInfo->sessionID,//会话标识
					pRspInfo->accountID,//客户号
					pRspInfo->errorID,//错误ID
					pRspInfo->localOrderID,//本地委托号
					pRspInfo->spdOrderID,//柜台委托号
					"登陆失败");//错误信息
		}
		printf("%s\n",rsp_msg);
	}
	//stock-登出响应
	virtual void OnRspStockUserLogout(DFITCSECRspUserLogoutField *pRspUserLogout, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		if ( pRspUserLogout)
		{
			sprintf(rsp_msg, "SEC-登出响应 : [请求ID]:[%ld],[客户号]:[%s],[结果]:[%ld],[返回信息]:[%s]",
					pRspUserLogout->requestID,//请求ID
					pRspUserLogout->accountID,//客户号
					pRspUserLogout->result,//结果
					"登出成功");//返回信息
		}
		if ( pRspInfo)
				{

					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							"登出失败");//错误信息
				}
		printf("%s\n",rsp_msg);
	}
	//stock-委托报单响应
	virtual void OnRspStockEntrustOrder(DFITCStockRspEntrustOrderField *pData, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		 if (pData)
		{
			sprintf(rsp_msg, "STOCK-委托响应: [请求ID]:[%ld],[客户号]:[%s],[本地委托号]:[%ld],[柜台委托号]:[%d],[委托批次号(N)]:[%d],[委托返回信息]:[%s]",
					pData->requestID,//请求ID
					pData->accountID,//客户号
					pData->localOrderID,//本地委托号
					pData->spdOrderID,//柜台委托号
					pData->entrustBatchID,//委托批次号(N)
					"委托成功");//委托返回信息
		}
		 if ( pRspInfo)
		 		{

		 			sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
		 					pRspInfo->requestID,//请求ID
		 					pRspInfo->sessionID,//会话标识
		 					pRspInfo->accountID,//客户号
		 					pRspInfo->errorID,//错误ID
		 					pRspInfo->localOrderID,//本地委托号
		 					pRspInfo->spdOrderID,//柜台委托号
		 					"委托失败");//错误信息
		 		}
		 printf("%s\n",rsp_msg);
	}
	//stock-委托撤单响应
	virtual void OnRspStockWithdrawOrder(DFITCSECRspWithdrawOrderField *pData, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		 if (pData)
		{
			sprintf(rsp_msg,"SEC-撤单响应: [请求ID]:[%ld],[客户号]:[%s],[本地委托号]:[%ld],[柜台委托号]:[%d],[委托时间]:[%s],[撤单返回信息]:[%s]",
					pData->requestID,//请求ID
					pData->accountID,//客户号
					pData->localOrderID,//本地委托号
					pData->spdOrderID,//柜台委托号
					pData->entrustTime,//委托时间
					"撤单成功");//撤单返回信息
		}
		 if ( pRspInfo)
		 		{

		 			sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
		 					pRspInfo->requestID,//请求ID
		 					pRspInfo->sessionID,//会话标识
		 					pRspInfo->accountID,//客户号
		 					pRspInfo->errorID,//错误ID
		 					pRspInfo->localOrderID,//本地委托号
		 					pRspInfo->spdOrderID,//柜台委托号
		 					"撤单失败");//错误信息
		 		}
		 printf("%s\n",rsp_msg);
	}
	//stock-委托查询响应
	virtual void OnRspStockQryEntrustOrder(DFITCStockRspQryEntrustOrderField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		char rsp_msg[4096] = {0};
		if (pData)
		{
			sprintf(rsp_msg,"STOCK-委托查询响应: [请求ID]:[%ld],[报盘股东号]:[%s],[币种]:[%s],[成交金额]:[%f],[成交价格]:[%f],[成交时间]:[%s],[成交数量]:[%d],[股东号]:[%s],[交易所代码]:[%s],[清算资金]:[%f],[委托方式]:[%d],[委托号]:[%d],[委托价格]:[%f],[委托类别]:[%d],[委托数量]:[%d],[证劵代码]:[%s],[证券类别]:[%s],[委托时间]:[%s],[申报时间]:[%s],[申报结果]:[%d],[撤销标志]:[%s],[冻结资金]:[%f],[客户号]:[%s],[撤单数量]:[%d],[申报委托号]:[%s],[订单类型]:[%d],[委托批次号]:[%d],[资金冻结流水号]:[%d],[证券冻结流水号]:[%d],[申报日期]:[%d],[申报记录号]:[%d],[委托日期]:[%d],[增量查询索引值]:[%s],[IP地址]:[%s],[MAC地址]:[%s]",
					pData->requestID,//请求ID
					pData->offerShareholderID,//报盘股东号
					pData->currency,//币种
					pData->turnover,//成交金额
					pData->tradePrice,//成交价格
					pData->tradeTime,//成交时间
					pData->tradeQty,//成交数量
					pData->shareholderID,//股东号
					pData->exchangeID,//交易所代码
					pData->clearFunds,//清算资金
					pData->entrustType,//委托方式
					pData->spdOrderID,//委托号
					pData->entrustPrice,//委托价格
					pData->entrustDirection,//委托类别
					pData->entrustQty,//委托数量
					pData->securityID,//证劵代码
					pData->securityType,//证券类别
					pData->entrustTime,//委托时间
					pData->declareTime,//申报时间
					pData->declareResult,//申报结果
					pData->withdrawFlag,//撤销标志
					pData->freezeFunds,//冻结资金
					pData->accountID,//客户号
					pData->withdrawQty,//撤单数量
					pData->declareOrderID,//申报委托号
					pData->orderType,//订单类型
					pData->entrustBatchID,//委托批次号
					pData->freezeFundsSerialID,//资金冻结流水号
					pData->freezeStockSerialID,//证券冻结流水号
					pData->declareDate,//申报日期
					pData->declareSerialID,//申报记录号
					pData->entrustDate,//委托日期
					pData->incQryIndex,//增量查询索引值
					pData->ipAddr,//IP地址
					pData->macAddr);//MAC地址
		}
		if ( pRspInfo)
				{

					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							"委托查询失败");//错误信息
				}
		 printf("%s\n",rsp_msg);
	}
	//stock-实时成交查询
	virtual void OnRspStockQryRealTimeTrade(DFITCStockRspQryRealTimeTradeField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		char rsp_msg[4096] = {0};
		 if (pData)
		 {
			 sprintf(rsp_msg,"STOCK-实时成交查询响应: [请求ID]:[%ld],[客户号]:[%s],[柜台委托号]:[%d],[申报委托号]:[%s],[交易所代码]:[%s],[股东号]:[%s],[委托类别]:[%d],[撤销标志]:[%s],[证券代码]:[%s],[证券名称]:[%s],[委托数量]:[%d],[委托价格]:[%f],[撤单数量]:[%d],[成交数量]:[%d],[成交金额]:[%f],[成交价格]:[%f],[成交时间]:[%s],[币种]:[%s],[清算资金]:[%f],[委托批次号]:[%d],[订单类型]:[%d]",
						pData->requestID,//请求ID
						pData->accountID,//客户号
						pData->spdOrderID,//柜台委托号
						pData->declareOrderID,//申报委托号
						pData->exchangeID,//交易所代码
						pData->shareholderID,//股东号
						pData->entrustDirection,//委托类别
						pData->withdrawFlag,//撤销标志
						pData->securityID,//证券代码
						pData->securityName,//证券名称
						pData->entrustQty,//委托数量
						pData->entrustPrice,//委托价格
						pData->withdrawQty,//撤单数量
						pData->tradeQty,//成交数量
						pData->turnover,//成交金额
						pData->tradePrice,//成交价格
						pData->tradeTime,//成交时间
						pData->currency,//币种
						pData->clearFunds,//清算资金
						pData->entrustBatchID,//委托批次号
						pData->orderType);//订单类型
		 }
		 if ( pRspInfo)
		 		{

		 			sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
		 					pRspInfo->requestID,//请求ID
		 					pRspInfo->sessionID,//会话标识
		 					pRspInfo->accountID,//客户号
		 					pRspInfo->errorID,//错误ID
		 					pRspInfo->localOrderID,//本地委托号
		 					pRspInfo->spdOrderID,//柜台委托号
		 					pRspInfo->errorMsg);//错误信息
		 		}
		 printf("%s\n",rsp_msg);
	}
	//stock-分笔成交查询响应
	virtual void OnRspStockQrySerialTrade(DFITCStockRspQrySerialTradeField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-分笔成交查询响应: [请求ID]:[%ld],[客户号]:[%s],[币种]:[%s],[成交编号]:[%s],[成交金额]:[%f],[成交价格]:[%f],[成交数量]:[%d],[股东号]:[%s],[交易所代码]:[%s],[清算资金]:[%f],[柜台委托号]:[%d],[委托类别]:[%d],[证券代码]:[%s],[证劵类别]:[%s],[证券名称]:[%s],[撤销标志]:[%s],[佣金]:[%f],[回报序号]:[%d],[利息报价]:[%f],[申报委托号]:[%s],[增量查询索引值]:[%s],[利息]:[%f],[成交时间]:[%s]",
					pData->requestID,//请求ID
					pData->accountID,//客户号
					pData->currency,//币种
					pData->tradeID,//成交编号
					pData->turnover,//成交金额
					pData->tradePrice,//成交价格
					pData->tradeQty,//成交数量
					pData->shareholderID,//股东号
					pData->exchangeID,//交易所代码
					pData->clearFunds,//清算资金
					pData->spdOrderID,//柜台委托号
					pData->entrustDirection,//委托类别
					pData->securityID,//证券代码
					pData->securityType,//证劵类别
					pData->securityName,//证券名称
					pData->withdrawFlag,//撤销标志
					pData->commission,//佣金
					pData->rtnSerialID,//回报序号
					pData->interestQuote,//利息报价
					pData->declareOrderID,//申报委托号
					pData->incQryIndex,//增量查询索引值
					pData->interest,//利息
					pData->tradeTime
					);
		}
		if ( pRspInfo)
				{

					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							pRspInfo->errorMsg);//错误信息
				}
		 printf("%s\n",rsp_msg);
	}
	//stock-持仓查询响应
	virtual void OnRspStockQryPosition(DFITCStockRspQryPositionField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-持仓查询响应: [请求ID]:[%ld],[客户号]:[%s],[币种]:[%s],[当日卖出成交金额]:[%f],[当日卖出成交数量]:[%d],[当日卖出委托数量]:[%d],[当日买入成交金额]:[%f],[当日买入成交数量]:[%d],[当日买入委托数量]:[%d],[非流通数量]:[%d],[股东号]:[%s],[交易所]:[%s],[开仓日期]:[%d],[可卖出数量]:[%d],[证券代码]:[%s],[证券类别]:[%s],[证券数量]:[%d],[今持仓量]:[%d],[未交收数量]:[%d],[变动日期:[%d],[可申购数量]:[%d],[可赎回数量]:[%d],[冻结数量]:[%d],[卖出抵消数量]:[%d],[买入抵消数量]:[%d],[申购成交数量]:[%d],[赎回成交数量]:[%d],[交易单位]:[%d],[累计卖出数量]:[%d],[累计买入数量]:[%d],[配股数量]:[%d],[申购数量]:[%d],[摊薄浮动盈亏]:[%f],[摊薄保本价]:[%f],[摊薄成本价]:[%f],[持仓均价]:[%f],[浮动盈亏]:[%f],[红利金额]:[%f],[累计浮动盈亏]:[%f],[卖出金额]:[%f],[买入金额]:[%f],[买入均价]:[%f],[配股金额]:[%f],[最新市值]:[%f],[保本价]:[%f],[最新价]:[%f],[非流通市值]:[%f],[利息报价]:[%f],[昨收盘价]:[%f]",
					pData->requestID,//请求ID
					pData->accountID,//客户号
					pData->currency,//币种
					pData->sellTurnover,//当日卖出成交金额
					pData->sellTradeQty,//当日卖出成交数量
					pData->sellEntrustQty,//当日卖出委托数量
					pData->buyTurnover,//当日买入成交金额
					pData->buyTradeQty,//当日买入成交数量
					pData->buyEntrustQty,//当日买入委托数量
					pData->nonCirculateQty,//非流通数量
					pData->shareholderID,//股东号
					pData->exchangeID,//交易所
					pData->openDate,//开仓日期
					pData->ableSellQty,//可卖出数量
					pData->securityID,//证券代码
					pData->securityType,//证券类别
					pData->securityQty,//证券数量
					pData->position,//今持仓量
					pData->unSettleQty,//未交收数量
					pData->changeDate,//变动日?
					pData->ablePurchaseQty,//可申购数量
					pData->ableRedemptionQty,//可赎回数量
					pData->freezeQty,//冻结数量
					pData->offsetSQty,//卖出抵消数量
					pData->offsetBQty,//买入抵消数量
					pData->purchaseTradeQty,//申购成交数量
					pData->redemptionTradeQty,//赎回成交数量
					pData->tradeUnit,//交易单位
					pData->totalSellQty,//累计卖出数量
					pData->totalBuyQty,//累计买入数量
					pData->rationedSharesQty,//配股数量
					pData->purchaseQty,//申购数量
					pData->dilutedFloatProfitLoss,//摊薄浮动盈亏
					pData->dilutedBreakevenPrice,//摊薄保本价
					pData->dilutedCost,//摊薄成本价
					pData->avgPositionPrice,//持仓均价
					pData->floatProfitLoss,//浮动盈亏
					pData->dividend,//红利金额
					pData->totalFloatProfitLoss,//累计浮动盈亏
					pData->sellAmount,//卖出金额
					pData->buyAmount,//买入金额
					pData->buyAvgPrice,//买入均价
					pData->rationedSharesAmount,//配股金额
					pData->latestMarket,//最新市值
					pData->breakevenPrice,//保本价
					pData->latestPrice,//最新价
					pData->nonCirculateMarket,//非流通市值
					pData->interestQuote,//利息报价
					pData->preClosePrice
					);
		}
		if ( pRspInfo)
				{
					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							"持仓查询失败");//错误信息
				}
		 printf("%s\n",rsp_msg);
	}
	//stock-客户资金查询响应
	virtual void OnRspStockQryCapitalAccountInfo(DFITCStockRspQryCapitalAccountField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-客户资金查询响应: [请求ID]:[%ld],[币种]:[%s],[可用资金]:[%f],[T+2可用资金]:[%f],[预计利息]:[%f],[账户余额]:[%f],[客户状态]:[%d],[客户号]:[%s],[冻结资金]:[%f],[T+2冻结资金]:[%f],[机构代码]:[%s],[总资金]:[%f],[总市值]:[%f]",
					pData->requestID,//请求ID
					pData->currency,//币种
					pData->availableFunds,//可用资金
					pData->t2AvailableFunds,//T+2可用资金
					pData->anticipatedInterest,//预计利息
					pData->accountBalance,//账户余额
					pData->accountStatus,//客户状态
					pData->accountID,//客户号
					pData->freezeFunds,//冻结资金
					pData->t2FreezeFunds,//T+2冻结资金
					pData->branchID,//机构代码
					pData->totalFunds,//总资金
					pData->totalMarket);//总市值
		}
		if ( pRspInfo)
				{

					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							pRspInfo->errorMsg);//错误信息
				}
		printf("%s\n",rsp_msg);
	}
	//stock-客户信息查询响应
	virtual void OnRspStockQryAccountInfo(DFITCStockRspQryAccountField *pData, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-客户信息查询响应: [请求ID]:[%ld],[电话]:[%s],[客户号]:[%s],[客户姓名]:[%s],[证件编号]:[%s],[证件类型]:[%d],[机构编码]:[%s],[移动电话]:[%s],[委托方式]:[%d],[客户状态]:[%d],[密码同步标志]:[%d]",
					pData->requestID,//请求ID
					pData->tel,//电话
					pData->accountID,//客户号
					pData->accountName,//客户姓名
					pData->accountIdentityID,//证件编号
					pData->accountIdentityType,//证件类型
					pData->branchID,//机构编码
					pData->mobile,//移动电话
					pData->entrustType,//委托方式
					pData->accountStatus,//客户状态
					pData->pwdSynFlag);//密码同步标志
		}
		if ( pRspInfo)
				{

					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							pRspInfo->errorMsg);//错误信息
				}
		printf("%s\n",rsp_msg);
	}
	//stock-股东信息查询响应
	virtual void OnRspStockQryShareholderInfo(DFITCStockRspQryShareholderField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-股东信息查询响应: [请求ID]:[%ld],[客户号]:[%s],[股东号]:[%s],[股东指定属性]:[%d],[交易权限]:[%d],[交易所]:[%s],[股东状态]:[%d],[主账户标志]:[%d],[股东控制属性]:[%d],[机构编码]:[%s],[股东类别]:[%d]",
					pData->requestID,//请求ID
					pData->account,//客户号
					pData->shareholderID,//股东号
					pData->shareholderSpecProp,//股东指定属性
					pData->tradePermissions,//交易权限
					pData->exchangeID,//交易所
					pData->shareholderStatus,//股东状态
					pData->mainAccountFlag,//主账户标志
					pData->shareholderCtlProp,//股东控制属性
					pData->branchID,//机构编码
					pData->shareholderType);//股东类别
		}
		if ( pRspInfo)
				{

					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							pRspInfo->errorMsg);//错误信息
				}
		printf("%s\n",rsp_msg);
	}
	//stock-资金调拨响应
	virtual void OnRspStockTransferFunds(DFITCStockRspTransferFundsField *pData,DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-资金调转响应: [请求ID]:[%ld],[客户号]:[%s],[流水号]:[%d],[账户余额]:[%f],[可用资金]:[%f],[T+2可用资金]:[%f],[资金调转标志]:[%d]",
					pData->requestID,//请求ID
					pData->accountID,//客户号
					pData->serialID,//流水号
					pData->accountBanlance,//账户余额
					pData->availableFunds,//可用资金
					pData->t2AvailableFunds,//T+2可用资金
					pData->fundsTransFlag);//资金调转标志
		}
		if ( pRspInfo)
				{

					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							pRspInfo->errorMsg);//错误信息
				}
		printf("%s\n",rsp_msg);
	}
	//stock-批量委托响应
	virtual void OnRspStockEntrustBatchOrder(DFITCStockRspEntrustBatchOrderField *pData, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-批量委托响应: [请求ID]:[%ld],[客户号]:[%s],[本地委托号]:[%ld],[委托号范围]:[%s],[委托批次号]:[%d],[成功委托笔数]:[%d]",
					pData->requestID,//请求ID
					pData->accountID,//客户号
					pData->localOrderID,//本地委托号
					pData->orderRangeID,//委托号范围
					pData->entrustBatchID,//委托批次号
					pData->sucEntrustCount);//成功委托笔数
		}
		if ( pRspInfo)
				{

					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							pRspInfo->errorMsg);//错误信息
				}
		printf("%s\n",rsp_msg);
	}
	//stock-批量撤单响应
	virtual void OnRspStockWithdrawBatchOrder(DFITCStockRspWithdrawBatchOrderField *pData, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-批量撤单响应: [请求ID]:[%ld],[客户号]:[%s],[撤单结果]:[%ld]",
					pData->requestID,//请求ID
					pData->accountID,//客户号
					pData->result);//撤单结果
		}
		if ( pRspInfo)
				{

					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							pRspInfo->errorMsg);//错误信息
				}
		printf("%s\n",rsp_msg);
	}
	//stock-计算可委托数量响应
	virtual void OnRspStockCalcAbleEntrustQty(DFITCStockRspCalcAbleEntrustQtyField *pData, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-计算可委托数量响应: [请求ID]:[%ld],[客户号]:[%s],[交易所代码]:[%s],[证券代码]:[%s],[可委托数量]:[%d]",
					pData->requestID,//请求ID
					pData->accountID,//客户号
					pData->exchangeID,//交易所代码
					pData->securityID,//证券代码
					pData->ableEntrustQty);//可委托数量
		}
		if ( pRspInfo)
				{

					sprintf(rsp_msg, "ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
							pRspInfo->requestID,//请求ID
							pRspInfo->sessionID,//会话标识
							pRspInfo->accountID,//客户号
							pRspInfo->errorID,//错误ID
							pRspInfo->localOrderID,//本地委托号
							pRspInfo->spdOrderID,//柜台委托号
							pRspInfo->errorMsg);//错误信息
				}
		printf("%s\n",rsp_msg);
	}
	//stock-委托回报响应
	virtual void OnStockEntrustOrderRtn(DFITCStockEntrustOrderRtnField * pData)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-委托回报: [本地委托号]:[%ld],[客户号]:[%s],[股东号]:[%s],[交易所代码]:[%s],[币种]:[%s],[证劵代码]:[%s],[证券类别]:[%s],[撤单数量]:[%d],[撤销标志]:[%s],[冻结资金]:[%f],[柜台委托号]:[%d],[委托类别]:[%d],[申报结果]:[%d],[委托数量]:[%d],[委托确认标志]:[%d],[委托时间]:[%s],[委托价格]:[%.3f]",
					pData->localOrderID,//本地委托号
					pData->accountID,//客户号
					pData->shareholderID,//股东号
					pData->exchangeID,//交易所代码
					pData->currency,//币种
					pData->securityID,//证劵代码
					pData->securityType,//证券类别
					pData->withdrawQty,//撤单数量
					pData->withdrawFlag,//撤销标志
					pData->freezeFunds,//冻结资金
					pData->spdOrderID,//柜台委托号
					pData->entrustDirection,//委托类别
					pData->declareResult,//申报结果
					pData->entrustQty,//委托数量
					pData->orderConfirmFlag,
					pData->entrustTime,
					pData->entrustPrice
					);
		}
		printf("%s\n",rsp_msg);
	}
	//stock-成交回报响应
	virtual void OnStockTradeRtn(DFITCStockTradeRtnField * pData)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-成交回报: [本地委托号]:[%ld],[客户号]:[%s],[股东号]:[%s],[交易所代码]:[%s],[币种]:[%s],[证劵代码]:[%s],[证券类别]:[%s],[撤销标志]:[%s],[成交编号]:[%s],[成交时间]:[%s],[撤单数量]:[%d],[柜台委托号]:[%d],[委托类别]:[%d],[清算资金]:[%f],[委托总成交数量]:[%d],[委托总成交金额]:[%f],[本次成交数量]:[%d],[本次成交价格]:[%f],[本次成交金额]:[%f],[委托数量]:[%d]",
					pData->localOrderID,//本地委托号
					pData->accountID,//客户号
					pData->shareholderID,//股东号
					pData->exchangeID,//交易所代码
					pData->currency,//币种
					pData->securityID,//证劵代码
					pData->securityType,//证券类别
					pData->withdrawFlag,//撤销标志
					pData->tradeID,//成交编号
					pData->tradeTime,//成交时间
					pData->withdrawQty,//撤单数量
					pData->spdOrderID,//柜台委托号
					pData->entrustDirection,//委托类别
					pData->clearFunds,//清算资金
					pData->totalTradeQty,//委托总成交数量
					pData->totalTurnover,//委托总成交金额
					pData->tradeQty,//本次成交数量
					pData->tradePrice,//本次成交价格
					pData->turnover,//本次成交金额
					pData->entrustQty);//委托数量
		}
		printf("%s\n",rsp_msg);
	}
	//stock-撤单回报响应
	virtual void OnStockWithdrawOrderRtn(DFITCStockWithdrawOrderRtnField * pData)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"STOCK-撤单回报: [本地委托号]:[%ld],[客户号]:[%s],[股东号]:[%s],[交易所代码]:[%s],[币种]:[%s],[证券代码]:[%s],[证券类别]:[%s],[撤单数量]:[%d],[成交数量]:[%d],[撤销标志]:[%s],[冻结资金]:[%f],[柜台委托号]:[%d],[委托类别]:[%d],[委托数量]:[%d]",
					pData->localOrderID,//本地委托号
					pData->accountID,//客户号
					pData->shareholderID,//股东号
					pData->exchangeID,//交易所代码
					pData->currency,//币种
					pData->securityID,//证券代码
					pData->securityType,//证券类别
					pData->withdrawQty,//撤单数量
					pData->tradeQty,//成交数量
					pData->withdrawFlag,//撤销标志
					pData->freezeFunds,//冻结资金
					pData->spdOrderID,//柜台委托号
					pData->entrustDirection,//委托类别
					pData->entrustQty);//委托数量
		}
		printf("%s\n",rsp_msg);
	}
	//sop-登陆响应
	virtual void OnRspSOPUserLogin(DFITCSECRspUserLoginField *pRspUserLogin, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		if(pRspUserLogin)
		{
			sprintf(rsp_msg, "SEC-登录响应 : [请求ID]:[%ld],[客户号]:[%s],[会话编号]:[%ld],[前置编号]:[%ld],[本地委托号]:[%ld],[登录时间]:[%s],[交易日]:[%d],[结果]:[%ld],[返回信息]:[%s]",
					pRspUserLogin->requestID,//请求ID
					pRspUserLogin->accountID,//客户号
					pRspUserLogin->sessionID,//会话编号
					pRspUserLogin->frontID,//前置编号
					pRspUserLogin->localOrderID,//本地委托号
					pRspUserLogin->loginTime,//登录时间
					pRspUserLogin->tradingDay,//交易日
					pRspUserLogin->result,//结果
					"登陆成功");//返回信息
		}
		if(pRspInfo)
		{
			sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
					pRspInfo->requestID,//请求ID
					pRspInfo->sessionID,//会话标识
					pRspInfo->accountID,//客户号
					pRspInfo->errorID,//错误ID
					pRspInfo->localOrderID,//本地委托号
					pRspInfo->spdOrderID,//柜台委托号
					"登陆失败");//错误信息
		}
		printf("%s\n",rsp_msg);
	}
	//sop-登出响应
	virtual void OnRspSOPUserLogout(DFITCSECRspUserLogoutField *pRspUserLogout, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		if(pRspUserLogout)
		{
			sprintf(rsp_msg,"SEC-登出响应 : [请求ID]:[%ld],[客户号]:[%s],[结果]:[%ld],[返回信息]:[%s]",
					pRspUserLogout->requestID,//请求ID
					pRspUserLogout->accountID,//客户号
					pRspUserLogout->result,//结果
					"登出成功");//返回信息
		}
		if(pRspInfo)
		{
			sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
					pRspInfo->requestID,//请求ID
					pRspInfo->sessionID,//会话标识
					pRspInfo->accountID,//客户号
					pRspInfo->errorID,//错误ID
					pRspInfo->localOrderID,//本地委托号
					pRspInfo->spdOrderID,//柜台委托号
					"登出失败");//错误信息
		}
		printf("%s\n",rsp_msg);
	}
	//sop-报单响应
	virtual void OnRspSOPEntrustOrder(DFITCSOPRspEntrustOrderField *pData, DFITCSECRspInfoField *pRspInfo)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"SOP-委托响应: [请求ID]:[%ld],[客户号]:[%s],[本地委托号]:[%ld],[柜台委托号]:[%d],[委托时间]:[%s],[冻结资金]:[%f]",
					pData->requestID,//请求ID
					pData->accountID,//客户号
					pData->localOrderID,//本地委托号
					pData->spdOrderID,//柜台委托号
					pData->entrustTime,//委托时间
					pData->freezeFunds);//冻结资金
		}
		if(pRspInfo)
		{
			sprintf(rsp_msg,"ERR-错误信息: [请求ID]:[%ld],[会话标识]:[%ld],[客户号]:[%s],[错误ID]:[%ld],[本地委托号]:[%ld],[柜台委托号]:[%d],[错误信息]:[%s]",
					pRspInfo->requestID,//请求ID
					pRspInfo->sessionID,//会话标识
					pRspInfo->accountID,//客户号
					pRspInfo->errorID,//错误ID
					pRspInfo->localOrderID,//本地委托号
					pRspInfo->spdOrderID,//柜台委托号
					"委托失败");//错误信息
		}
		printf("%s\n",rsp_msg);
	}

	//sop-委托回报响应
	virtual void OnSOPEntrustOrderRtn(DFITCSOPEntrustOrderRtnField * pData)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg,"SOP-委托回报: [本地委托号]:[%ld],[客户号]:[%s],[机构代码]:[%s],[股东号]:[%s],[交易所]:[%s],[证劵代码]:[%s],[撤销标志]:[%s],[币种]:[%s],[柜台委托号]:[%d],[委托类别]:[%d],[开平标志]:[%d],[委托价格]:[%.4f],[委托数量]:[%d],[申报结果]:[%d]",
					pData->localOrderID,//本地委托号
					pData->accountID,//客户号
					pData->branchID,//机构代码
					pData->shareholderID,//股东号
					pData->exchangeID,//交易所
					pData->securityID,//证劵代码
					pData->withdrawFlag,//撤销标志
					pData->currency,//币种
					pData->spdOrderID,//柜台委托号
					pData->entrustDirection,//委托类别
					pData->openCloseFlag,//开平标志
					pData->entrustPrice,//委托价格
					pData->entrustQty,//委托数量
					pData->declareResult);//申报结果
		}
		printf("%s\n",rsp_msg);
	}
	//sop-成交回报
	virtual void OnSOPTradeRtn(DFITCSOPTradeRtnField * pData)
	{
		char rsp_msg[4096] = {0};
		if(pData)
		{
			sprintf(rsp_msg, "SOP-成交回报: [本地委托号]:[%ld],[客户号]:[%s],[股东号]:[%s],[交易所]:[%s],[证劵代码]:[%s],[撤销标志]:[%s],[币种]:[%s],[柜台委托号]:[%d],[委托类别]:[%d],[开平标志]:[%d],[委托单类别]:[%d],[成交价格]:[%.4f],[成交数量]:[%d],[成交编号]:[%s]",
					pData->localOrderID,//本地委托号
					pData->accountID,//客户号
					pData->shareholderID,//股东号
					pData->exchangeID,//交易所
					pData->securityID,//证劵代码
					pData->withdrawFlag,//撤销标志
					pData->currency,//币种
					pData->spdOrderID,//柜台委托号
					pData->entrustDirection,//委托类别
					pData->openCloseFlag,//开平标志
					pData->orderCategory,//委托单类别
					pData->tradePrice,//成交价格
					pData->tradeQty,//成交数量
					pData->tradeID);//成交编号
		}
		printf("%s\n",rsp_msg);
	}
	/*//sop-
	virtual void OnRspStockQryShareholderInfo(DFITCStockRspQryShareholderField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		if(pData)
		{
			sprintf(GTM::rsp_msg,
		}
		if(pRspInfo)
		{
			sprintf(GTM::rsp_msg,
		}
		COut::out(GTM::rsp_msg);
	}
	//stock-
	virtual void OnRspStockQryShareholderInfo(DFITCStockRspQryShareholderField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		if(pData)
		{
			sprintf(GTM::rsp_msg,
		}
		if(pRspInfo)
		{
			sprintf(GTM::rsp_msg,
		}
		COut::out(GTM::rsp_msg);
	}
	//stock-
	virtual void OnRspStockQryShareholderInfo(DFITCStockRspQryShareholderField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		if(pData)
		{
			sprintf(GTM::rsp_msg,
		}
		if(pRspInfo)
		{
			sprintf(GTM::rsp_msg,
		}
		COut::out(GTM::rsp_msg);
	}
	//stock-
	virtual void OnRspStockQryShareholderInfo(DFITCStockRspQryShareholderField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		if(pData)
		{
			sprintf(GTM::rsp_msg,
		}
		if(pRspInfo)
		{
			sprintf(GTM::rsp_msg,
		}
		COut::out(GTM::rsp_msg);
	}
	//stock-
	virtual void OnRspStockQryShareholderInfo(DFITCStockRspQryShareholderField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		if(pData)
		{
			sprintf(GTM::rsp_msg,
		}
		if(pRspInfo)
		{
			sprintf(GTM::rsp_msg,
		}
		COut::out(GTM::rsp_msg);
	}
	//stock-
	virtual void OnRspStockQryShareholderInfo(DFITCStockRspQryShareholderField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		if(pData)
		{
			sprintf(GTM::rsp_msg,
		}
		if(pRspInfo)
		{
			sprintf(GTM::rsp_msg,
		}
		COut::out(GTM::rsp_msg);
	}
	//stock-
	virtual void OnRspStockQryShareholderInfo(DFITCStockRspQryShareholderField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		if(pData)
		{
			sprintf(GTM::rsp_msg,
		}
		if(pRspInfo)
		{
			sprintf(GTM::rsp_msg,
		}
		COut::out(GTM::rsp_msg);
	}
	//stock-
	virtual void OnRspStockQryShareholderInfo(DFITCStockRspQryShareholderField *pData, DFITCSECRspInfoField *pRspInfo, bool bIsLast)
	{
		if(pData)
		{
			sprintf(GTM::rsp_msg,
		}
		if(pRspInfo)
		{
			sprintf(GTM::rsp_msg,
		}
		COut::out(GTM::rsp_msg);
	}
*/
};

int main()
{
	std::string host;
	std::string Mdhost;
	CInput		in;
	CMdInput    Mdin;
	char		os_msg[256] = {0};
	int         change;

	//COut::create("rsp_data.log");
	//COut::os_bit(os_msg);
	//printf("This is %s running\n\n", os_msg);

	while (true)
	{

			printf("1.连接交易前置  ");
			printf("2.连接行情前置  ");
			printf("*.退出程勋请按任意数字\n");
			printf("请输入您的选择\n");
			scanf("%d",&change);
			switch(change)
			{

			case 1:
				if (in.FieldInput(CInput::_host, host))
				{
					DFITCSECTraderApi *pTraderApi=DFITCSECTraderApi::CreateDFITCSECTraderApi(NULL);
					if (pTraderApi)
					{
						JYHandler  Traderspi;
						while(1)
						{
							if ( 0== pTraderApi->Init((char *)(host.c_str()), &Traderspi))
							{
								in.func_usage(*pTraderApi);
							}
							break;
						}
						pTraderApi->Release();
						break;
					}
				}

			case 2:
					if (Mdin.FieldInput(CMdInput::_host, Mdhost))
					{
						DFITCSECMdApi *pMdApi=DFITCSECMdApi::CreateDFITCMdApi(NULL);
						if (pMdApi)
						{
							HQHandler         Mdspi;
							while(1)
							{
								if ( 0== pMdApi->Init((char *)(Mdhost.c_str()), &Mdspi))
								{
									Mdin.func_usage(*pMdApi);
								}
								break;
							}
							pMdApi->Release();
							break;
						}
					}
				default:
					return 0;
			}
	}
	//COut::destroy();
	return 0;
}


