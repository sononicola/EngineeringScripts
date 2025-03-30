import numpy as np

# Import all modules required to access RFEM
from RFEM.enums import (
    AddOn,
    StaticAnalysisType,
    ActionCategoryType,
    NodeReferenceType,
    MemberLoadDirection,
    NodalSupportType,
    ObjectTypes,
    TimberServiceClassServiceClass,
    DesignSituationType,
    CaseObjectType,
)
from RFEM.initModel import Model, SetAddonStatus, Calculate_all
from RFEM.LoadCasesAndCombinations.loadCasesAndCombinations import (
    LoadCasesAndCombinations,
)
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.line import Line
from RFEM.BasicObjects.member import Member
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.Loads.memberLoad import MemberLoad

# importing modules requiered for timber design
from RFEM.TimberDesign.timberUltimateConfigurations import (
    TimberDesignUltimateConfigurations,
)
from RFEM.TimberDesign.timberServiceLimitStateConfigurations import (
    TimberDesignServiceLimitStateConfigurations,
)
from RFEM.TypesForTimberDesign.timberServiceClass import TimberServiceClass
from RFEM.LoadCasesAndCombinations.combinationWizard import CombinationWizard
from RFEM.LoadCasesAndCombinations.designSituation import DesignSituation
from RFEM.TypesForTimberDesign.timberEffectiveLengths import TimberEffectiveLengths
from RFEM.Tools.GetObjectNumbersByType import GetObjectNumbersByType
from RFEM.Results.resultTables import ResultTables, GetMaxValue, GetMinValue
import enum


def getMaxMinValue(structured_results: ResultTables, parameter: str) -> float:
    "This is a wrapper of RFEM.Results.resulTables.GetMinValue and RFEM.Results.resulTables.GetMaxValue"
    if abs(GetMinValue(structured_results, parameter)) > abs(
        GetMaxValue(structured_results, parameter)
    ):
        return GetMinValue(structured_results, parameter)
    else:
        return GetMaxValue(structured_results, parameter)


def getResultsPerMember(
    loading_type: CaseObjectType, loading_no: int = 1
) -> list[dict[str, float]]:
    "Return a list of dictionaries with all relevant results for each member in the model"
    listOfResults: list[dict[str, float]] = []
    member_no = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_MEMBER)

    for member in member_no:
        results: dict[str, float] = {}
        results["loading_type"] = loading_type
        results["loading_no"] = loading_no
        results["member number"] = member
        dispTable = ResultTables.MembersLocalDeformations(
            loading_type, loading_no, member
        )
        results["Maximum Deformation (abs) (mm)"] = round(
            getMaxMinValue(dispTable, "displacement_absolute") * 1000, 3
        )
        results["Maximum Deformation (in x) (mm)"] = round(
            getMaxMinValue(dispTable, "displacement_x") * 1000, 3
        )
        results["Maximum Deformation (in y) (mm)"] = round(
            getMaxMinValue(dispTable, "displacement_y") * 1000, 3
        )
        results["Maximum Deformation (in z) (mm)"] = round(
            getMaxMinValue(dispTable, "displacement_z") * 1000, 3
        )

        momentTable = ResultTables.MembersInternalForces(
            loading_type, loading_no, member
        )
        results["Maximum Internal Force (N) (kN)"] = round(
            getMaxMinValue(momentTable, "internal_force_n") / 1000, 3
        )
        results["Maximum Internal Force (Vy) (kN)"] = round(
            getMaxMinValue(momentTable, "internal_force_vy") / 1000, 3
        )
        results["Maximum Internal Force (Vz) (kN)"] = round(
            getMaxMinValue(momentTable, "internal_force_vz") / 1000, 3
        )
        results["Maximum Internal Moment (Mt) (kNm)"] = round(
            getMaxMinValue(momentTable, "internal_force_mt") / 1000, 3
        )
        results["Maximum Internal Moment (My) (kNm)"] = round(
            getMaxMinValue(momentTable, "internal_force_my") / 1000, 3
        )
        results["Maximum Internal Moment (Mz) (kNm)"] = round(
            getMaxMinValue(momentTable, "internal_force_mz") / 1000, 3
        )

        listOfResults.append(results)

    return listOfResults


def getResultsLinesSupport(
    loading_type: CaseObjectType, loading_no: int = 1
) -> list[dict[str, float]]:
    "Return a list of dictionaries with all line's support actions"
    listOfResults: list[dict[str, float]] = []
    line_no = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_LINE)
    print(line_no)
    for line in line_no:
        dispTable: list[dict[str, float]] = ResultTables.LinesSupportForces(
            loading_type, loading_no, line
        )
        for dct in dispTable:
            dct.update({"loading_type": loading_type, "loading_no": loading_no})

            listOfResults.append(dct)

    return listOfResults
