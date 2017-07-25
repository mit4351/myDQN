#!/usr/bin/python
# -*- coding: utf-8^[ -*-

from rlglue.utils import TaskSpecVRLGLUE3

ts ="""VERSION RL-Glue-3.0 PROBLEMTYPE episodic DISCOUNTFACTOR .7   """

ts +=""" OBSERVATIONS INTS (NEGINF 1) ( 2 -5 POSINF ) DOUBLES (2 -1.2 0.5 )(-.07 .07) (UNSPEC 3.3) (0 100.5) CHARCOUNT 32 """
#ts +=""" ACTIONS INTS (5 0 4) DOUBLES (-.5 2) (2 7.8 9) (NEGINF UNSPEC) REWARDS (-5.0 5.0) EXTRA some other stuff goes here"""

print(ts)
TaskSpec = TaskSpecVRLGLUE3.TaskSpecParser(ts)

if TaskSpec.valid:
   print( "=======================================================================================================")
   print( "Version: ["+TaskSpec.getVersion()+"]")
   print( "ProblemType: ["+TaskSpec.getProblemType()+"]")
   print( "DiscountFactor: ["+str(TaskSpec.getDiscountFactor())+"]")
   print( "=======================================================================================================")
   print( "\t \t \t \t Observations")
   print( "=======================================================================================================")
   print( "Observations: ["+TaskSpec.getObservations()+"]")
   print( "Integers:",TaskSpec.getIntObservations())
   print( "Doubles: ",TaskSpec.getDoubleObservations())
   print( "Chars:   ",TaskSpec.getCharCountObservations())
   print( "=======================================================================================================")
   print( "\t \t \t \t Actions")
   print( "======================================================================================================")
   print( "Actions: ["+TaskSpec.getActions()+"]")
   print( "Integers:",TaskSpec.getIntActions())
   print( "Doubles: ",TaskSpec.getDoubleActions())
   print( "Chars:   ",TaskSpec.getCharCountActions())
   print( "=======================================================================================================")
   print( "Reward :["+TaskSpec.getReward()+"]")
   print( "Reward Range:",TaskSpec.getRewardRange())
   print( "Extra: ["+TaskSpec.getExtra()+"]")
   print( "remeber that by using len() you get the cardinality of lists!")
   print( "Thus:")
   print( "len(",TaskSpec.getDoubleObservations(),") ==> ",len(TaskSpec.getDoubleObservations())," Double Observations")
   print( TaskSpec.isSpecial("NEGINF"))

