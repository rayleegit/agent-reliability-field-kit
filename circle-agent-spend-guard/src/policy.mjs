const MONEY_MOVEMENT = [
  /^circle services pay\b/,
  /^circle wallet transfer\b/,
  /^circle bridge transfer\b/,
  /^circle gateway deposit\b/,
  /^circle wallet sign\b/,
  /^circle wallet limit set\b/,
];

function roundUsd(value) {
  return Math.round((value + Number.EPSILON) * 100) / 100;
}

export function isMoneyMovement(command) {
  return MONEY_MOVEMENT.some((pattern) => pattern.test(command.trim()));
}

export function spentToday(ledger, date) {
  return roundUsd(
    ledger
      .filter((entry) => entry.status === "executed" && entry.date === date)
      .reduce((total, entry) => total + entry.amountUsd, 0),
  );
}

export function planAction({ action, policy, ledger = [] }) {
  const command = action.command.trim();

  if (!isMoneyMovement(command)) {
    return {
      decision: "allow",
      reason: "Read-only or non-payment command.",
      requiresHumanApproval: false,
    };
  }

  if (!Number.isFinite(action.amountUsd) || action.amountUsd <= 0) {
    return {
      decision: "block",
      reason: "Money movement requires an explicit positive amount.",
      requiresHumanApproval: false,
    };
  }

  if (action.amountUsd > policy.perTransactionUsd) {
    return {
      decision: "block",
      reason: `Amount exceeds the $${policy.perTransactionUsd.toFixed(2)} per-transaction cap.`,
      requiresHumanApproval: false,
    };
  }

  if (!policy.allowedDestinations.includes(action.destination)) {
    return {
      decision: "block",
      reason: "Destination is not allowlisted.",
      requiresHumanApproval: false,
    };
  }

  const currentDailySpend = spentToday(ledger, action.date);
  const projectedDailySpend = roundUsd(currentDailySpend + action.amountUsd);
  if (projectedDailySpend > policy.dailyUsd) {
    return {
      decision: "block",
      reason: `Projected daily spend $${projectedDailySpend.toFixed(2)} exceeds the $${policy.dailyUsd.toFixed(2)} cap.`,
      requiresHumanApproval: false,
    };
  }

  return {
    decision: "require_approval",
    reason: "Money movement is within policy but requires a human decision.",
    requiresHumanApproval: true,
    approvalPrompt: {
      command,
      destination: action.destination,
      amountUsd: roundUsd(action.amountUsd),
      projectedDailySpend,
    },
  };
}

export function executeApproved({ action, plan, approval, ledger = [] }) {
  if (plan.decision !== "require_approval") {
    throw new Error("Only a policy-approved payment plan can be executed.");
  }

  if (!approval || approval.approved !== true || !approval.approvedBy) {
    throw new Error("Explicit human approval with an approver identity is required.");
  }

  const receipt = {
    id: `demo_${String(ledger.length + 1).padStart(3, "0")}`,
    date: action.date,
    command: action.command.trim(),
    destination: action.destination,
    amountUsd: roundUsd(action.amountUsd),
    approvedBy: approval.approvedBy,
    status: "executed",
    network: "offline-demo",
  };

  return { receipt, ledger: [...ledger, receipt] };
}
