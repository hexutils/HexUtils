#include <cstdlib>
#include <regex>
#include "TUtilHelpers.hh"


void TUtilHelpers::ExpandEnvironmentVariables(std::string& str){
  // Take care of special characters
  size_t ipos;
  std::string strTakeOut, strPutIn;

  strTakeOut = ".oODOLLAROo.";
  strPutIn = "$";
  ipos = str.find(strTakeOut);
  while (ipos!=std::string::npos){ str.replace(ipos, strTakeOut.length(), strPutIn.c_str()); ipos = str.find(strTakeOut); }
  strTakeOut = ".oOOPEN_BRACKETOo.";
  strPutIn = "{";
  ipos = str.find(strTakeOut);
  while (ipos!=std::string::npos){ str.replace(ipos, strTakeOut.length(), strPutIn.c_str()); ipos = str.find(strTakeOut); }
  strTakeOut = ".oOCLOSE_BRACKETOo.";
  strPutIn = "}";
  ipos = str.find(strTakeOut);
  while (ipos!=std::string::npos){ str.replace(ipos, strTakeOut.length(), strPutIn.c_str()); ipos = str.find(strTakeOut); }

  static std::regex env("\\$\\{([^}]+)\\}");
  std::smatch match;
  while (std::regex_search(str, match, env)){
    const char* s = getenv(match[1].str().c_str());
    const std::string var(s == NULL ? "" : s);
    str.replace(match[0].first, match[0].second, var);
  }
}
