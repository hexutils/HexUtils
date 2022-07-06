#ifndef MELAHXSWIDTH_H
#define MELAHXSWIDTH_H

#include <string>
#include "TGraph.h"
#include "TSpline.h"
#include "TVar.hh"


class MELAHXSWidth{
public:
  MELAHXSWidth(std::string fileLoc = "../txtFiles", std::string strAppend="YR3", TVar::VerbosityLevel verbosity_=TVar::ERROR);
  MELAHXSWidth(const MELAHXSWidth& other);
  ~MELAHXSWidth();
  double HiggsWidth(double mH) const;

protected:
  std::string fileName;
  std::vector<double> mass_BR;
  std::vector<double> BR;
  double* xmhW;
  double* sigW;
  TGraph* graphW;
  TSpline3* gsW;

  TVar::VerbosityLevel verbosity;

  void build();

};

#endif

