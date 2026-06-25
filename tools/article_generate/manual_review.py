import logging

logger = logging.getLogger(__name__)


def manual_review(state: dict):
    """
    人工审核节点

    工作流会在执行到此节点前暂停（通过 interrupt_before 配置），
    等待外部通过 workflow.update_state() 注入审核结果后继续执行。

    审核结果通过 workflow.update_state() 设置：
    - manual_review_result: "pass" 或 "reject"
    - reject_reason: 驳回原因（仅 reject 时需要）
    """
    logger.info("进入节点: manual_review")

    # 从 state 中获取外部注入的审核结果
    manual_review_result = state.get("manual_review_result")
    reject_reason = state.get("reject_reason", "")

    if manual_review_result == "pass":
        logger.info("人工审核结果: 通过")
        return {"manual_review_result": True}
    elif manual_review_result == "reject":
        logger.info(f"人工审核结果: 驳回, 原因: {reject_reason}")
        return {"manual_review_result": False, "reject_reason": reject_reason}
    else:
        # 未收到审核结果，默认通过
        logger.warning("未收到人工审核结果，默认通过")
        return {"manual_review_result": True}
