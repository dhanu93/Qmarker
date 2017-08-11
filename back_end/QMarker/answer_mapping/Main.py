from answer_mapping.answerMapping import answerMapping
from postagging.views import postagger
from ner.views import nerTagging
from scoring.marking_tab import  MarkAnswer
from scoring.teacher_marking_tab import ScoreRfinement

import json

compareAnswerObj = answerMapping()
postaggerObject = postagger()
nerTaggingObject = nerTagging()
markAnswerObject = MarkAnswer()
scoreRfinementObject = ScoreRfinement()

class QmarkerMain:

    def compareTwoAnswers(self,sent1,sent2,qid):
        # sent1 = 'Bears are climbers despite their bulk.'
        # sent2 = 'Gaining output using force.'

        # triplet creation
        tripletObj1 = postaggerObject.extraxtedTriplets(sent1)
        tripletObj2 = postaggerObject.extraxtedTriplets(sent2)

        # ner creation
        nerObj1 = nerTaggingObject.settingNER(tripletObj1)
        nerObj2 = nerTaggingObject.settingNER(tripletObj2)

        # answer matching
        markObj = compareAnswerObj.compareAnswersAndReturnMatchingPairs(nerObj1,nerObj2)

        # mark allocation
        finalMark = markAnswerObject.MarkSentences(markObj,qid)
        print("================================================================================")
        # print(round(finalMark,1))
        return finalMark



    def compareTwoAnswersAndGetSentenseComparisonData(self,sent1,sent2):
        # sent1 = 'Bears are climbers despite their bulk.'
        # sent2 = 'Gaining output using force.'

        # triplet creation
        tripletObj1 = postaggerObject.extraxtedTriplets(sent1)
        tripletObj2 = postaggerObject.extraxtedTriplets(sent2)

        # ner creation
        nerObj1 = nerTaggingObject.settingNER(tripletObj1)
        nerObj2 = nerTaggingObject.settingNER(tripletObj2)

        # answer matching
        markObj = compareAnswerObj.compareAnswersAndReturnMatchingPairs(nerObj1,nerObj2)

        return markObj