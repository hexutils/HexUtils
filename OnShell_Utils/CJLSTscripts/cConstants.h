#ifndef CCONSTANTS_H
#define CCONSTANTS_H

#include <TSpline.h>
#include <TString.h>
#include <memory>

class cConstantSpline {
  public:
    cConstantSpline(const TString& filename);
    void initspline(bool isDbkg);
    double eval(double ZZMass, bool isDbkg);
  private:
    const TString filename_;
    std::unique_ptr<TSpline3> spline_;
};

float getDVBF2jetsConstant(float ZZMass);
float getDVBF1jetConstant(float ZZMass);
float getDWHhConstant(float ZZMass);
float getDZHhConstant(float ZZMass);

float getDVBF2jetsWP(float ZZMass, bool useQGTagging);
float getDVBF1jetWP(float ZZMass, bool useQGTagging);
float getDWHhWP(float ZZMass, bool useQGTagging);
float getDZHhWP(float ZZMass, bool useQGTagging);

float getDVBF2jetsConstant_shiftWP(float ZZMass, bool useQGTagging, float newWP);
float getDVBF1jetConstant_shiftWP(float ZZMass, bool useQGTagging, float newWP);
float getDWHhConstant_shiftWP(float ZZMass, bool useQGTagging, float newWP);
float getDZHhConstant_shiftWP(float ZZMass, bool useQGTagging, float newWP);

float getDbkgVBFdecConstant(int ZZflav, float ZZMass);
float getDbkgVHdecConstant(int ZZflav, float ZZMass);

float getDbkgkinConstant(int ZZflav, float ZZMass);
float getDbkgConstant(int ZZflav, float ZZMass);

#endif
