cmake_minimum_required(VERSION 2.8)
project(AQ_ctp_api)

# 设置使用的编译器
set(CMAKE_BUILD_TYPE "Release")
if (CMAKE_COMPILER_IS_GNUC OR CMAKE_COMPILER_IS_GNUCXX) 
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -std=c++11")
endif ()

# 设置输出目录
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR}/lib)

# 使用64位编译
option(USE_64BITS "comiple 64bits" ON)
if (USE_64BITS)
  add_definitions(-DUSE_64BITS)
  #set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -m32")
  #set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -m32")
endif()

# 设置C++ API源文件的所在目录
if (UNIX)
    message("Under unix: " ${CMAKE_SIZEOF_VOID_P})
    if (CMAKE_SIZEOF_VOID_P MATCHES "8")
        set(CTPAPI_PATH ctpapi/x64_linux)
    endif()
endif()
include_directories(${CTPAPI_PATH})
set(CTPAPI_LIBRARY )
find_library(CTPAPI_MD_LIBRARY
  NAMES thostmduserapi
  PATHS ${CTPAPI_PATH}) 
find_library(CTPAPI_TD_LIBRARY
  NAMES thosttraderapi
  PATHS ${CTPAPI_PATH})


# 设置编译源文件
set (AQctpmd )
set (AQctptd )

option(BUILD_CTP_MD "build ctp md" ON)
if (BUILD_CTP_MD)
  add_definitions(-DBUILD_CTP_MD)
  set(CTP_MD_PATH AQctpmd/AQctpmd)
  include_directories(CTP_MD_PATH)
  set(VN_CTP_MD_SOURCE ${CMAKE_CURRENT_SOURCE_DIR}/AQctpmd/AQctpmd/AQctpmd.cpp)
  add_library(AQctpmd SHARED ${VN_CTP_MD_SOURCE})
endif()
option(BUILD_CTP_TD "build ctp td" ON)
if (BUILD_CTP_TD)
  add_definitions(-DBUILD_CTP_TD)
  set(CTP_TD_PATH AQctptd/AQctptd)
  include_directories(CTP_TD_PATH)
  set(VN_CTP_TD_SOURCE ${CMAKE_CURRENT_SOURCE_DIR}/AQctptd/AQctptd/AQctptd.cpp)
  add_library(AQctptd SHARED ${VN_CTP_TD_SOURCE})  
endif()

# 设置Python所在的目录
set(PYTHON_LIBRARY )
if (UNIX)
set(PYTHON_INCLUDE_PATH /home/zhanggao/anaconda3/include/bin)
find_library(PYTHON_LIBRARY
  NAMES python3.5m
  PATHS /usr/lib/x86_64-linux-gnu)
include_directories(${PYTHON_INCLUDE_PATH})
endif()

# 链接boost库，anaconda
set(Boost_USE_MULTITHREADED      ON)
find_package(Boost 1.66.0 COMPONENTS python locale thread date_time system chrono REQUIRED) # 如果boost库没有完全编译，需要将编译的库明确地指出，否者message(${Boost_LIBRARIES})会出错
if(Boost_FOUND)
  include_directories(/usr/local/lib)
  include_directories(/home/zhanggao/tools/boost_1_66_0/boost)
endif()

# 去掉生成的so文件名中前缀的lib
set_target_properties(AQctpmd PROPERTIES PREFIX "")

# 链接生成.so文件
target_link_libraries(AQctpmd  ${Boost_LIBRARIES} ${PYTHON_LIBRARY} ${CTPAPI_MD_LIBRARY})

# 和上面的MD相同
set_target_properties(AQctptd PROPERTIES PREFIX "")
target_link_libraries(AQctptd  ${Boost_LIBRARIES} ${PYTHON_LIBRARY} ${CTPAPI_TD_LIBRARY})



