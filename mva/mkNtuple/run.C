#include "makeTuple.h"
R__LOAD_LIBRARY(makeTuple.C+)

void run( const char* input_name, const std::string output_name )
{
   gROOT->ProcessLine("gErrorIgnoreLevel = kFatal;");
   gSystem->CompileMacro("makeTuple.C");

   TChain chain("tree");
   chain.Add(input_name);
   makeTuple t(&chain);
   t.Loop(output_name);
}
