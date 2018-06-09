CPP      = g++
CPPFLAGS = -I../include
LIBDIR   = ../lib

TARGET = DFITC_SEC_Demo
OBJS   = ApiDemo.o

$(TARGET): $(OBJS)
	$(CPP) -o $@ $^ $(LIBDIR)/libDFITCSECMdApi.so $(LIBDIR)/libDFITCSECTraderApi.so

ApiDemo.o: ApiDemo.cpp
	$(CPP) $(CPPFLAGS) -c -o $@ $<

.PHONY: all clean

clean:
	rm -rf $(OBJS) $(TARGET)