import io
import icu
import json

class HanComparator:
    dbObj = None

    def __init__(self):
        with io.open("data/Unihan_IRGSources.json", "r", encoding = "utf-8") as u:
            self.dbObj = json.loads(u.read())
            u.close()
    
    # 2.1.2 Sorting Algorithm Used by the Radical-Stroke Charts.
    # https://www.unicode.org/reports/tr38/#SortingAlgorithm
    def getCollationKey(self, hanChar):
        key = ord(hanChar) # start with bit 0-19
        blockID = icu.Char.ublock_getCode(hanChar) # bit 20-27
        if blockID == getattr(icu.UBlockCode, "CJK_UNIFIED_IDEOGRAPHS_EXTENSION_A"):
            key += 1 << 20
        elif blockID == getattr(icu.UBlockCode, "CJK_UNIFIED_IDEOGRAPHS_EXTENSION_B"):
            key += 2 << 20
        elif blockID == getattr(icu.UBlockCode, "CJK_UNIFIED_IDEOGRAPHS_EXTENSION_C"):
            key += 3 << 20
        elif blockID == getattr(icu.UBlockCode, "CJK_UNIFIED_IDEOGRAPHS_EXTENSION_D"):
            key += 4 << 20
        elif blockID == getattr(icu.UBlockCode, "CJK_UNIFIED_IDEOGRAPHS_EXTENSION_E"):
            key += 5 << 20
        elif blockID == getattr(icu.UBlockCode, "CJK_UNIFIED_IDEOGRAPHS_EXTENSION_F"):
            key += 6 << 20
        elif blockID == getattr(icu.UBlockCode, "CJK_UNIFIED_IDEOGRAPHS_EXTENSION_G"):
            key += 7 << 20
        elif blockID == getattr(icu.UBlockCode, "CJK_COMPATIBILITY_IDEOGRAPHS"):
            key += 254 << 20
        elif blockID == getattr(icu.UBlockCode, "CJK_COMPATIBILITY_IDEOGRAPHS_SUPPLEMENT"):
            key += 255 << 20
        # for main block or else, nothing to add

        rscode = self.dbObj[hanChar]["kRSUnicode"][0] # only first value because no way to choose
        tokens = rscode.split(".")
        if tokens[0].endswith("'"):
            tokens[0] = tokens[0][:-1]
            key += 1 << 28 # bit 28-31
        # bit 32-35, just do nothing right now
        if (stroke := int(tokens[1])) > 0: # it can be negative
            key += stroke << 36 # bit 36-43
        key += int(tokens[0]) << 44 # bit 44-51
        return key
