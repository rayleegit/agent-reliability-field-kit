import test from "node:test";
import assert from "node:assert/strict";

import {
  executeApproved,
  isMoneyMovement,
  planAction,
  spentToday,
} from "../src/policy.mjs";

const policy = {
  perTransactionUsd: 1,
  dailyUsd: 3,
  allowedDestinations: ["marketplace:research-api"],
};

const payment = {
  date: "2026-10-23",
  command: "circle services pay --service research-api --amount 0.25",
  destination: "marketplace:research-api",
  amountUsd: 0.25,
};

test("allows Circle discovery without approval", () => {
  const plan = planAction({
    action: {
      date: payment.date,
      command: "circle services search research",
      destination: "none",
      amountUsd: 0,
    },
    policy,
  });
  assert.equal(plan.decision, "allow");
  assert.equal(plan.requiresHumanApproval, false);
});

test("recognizes all guarded Circle command families", () => {
  assert.equal(isMoneyMovement("circle services pay --service example"), true);
  assert.equal(isMoneyMovement("circle wallet transfer --to 0xabc"), true);
  assert.equal(isMoneyMovement("circle bridge transfer --to-chain arc"), true);
  assert.equal(isMoneyMovement("circle gateway deposit --amount 1"), true);
  assert.equal(isMoneyMovement("circle wallet sign --payload demo"), true);
  assert.equal(isMoneyMovement("circle wallet limit set --daily 3"), true);
});

test("requires human approval for an in-policy payment", () => {
  const plan = planAction({ action: payment, policy });
  assert.equal(plan.decision, "require_approval");
  assert.equal(plan.approvalPrompt.amountUsd, 0.25);
});

test("blocks payments over the per-transaction cap", () => {
  const plan = planAction({
    action: { ...payment, amountUsd: 1.01 },
    policy,
  });
  assert.equal(plan.decision, "block");
  assert.match(plan.reason, /per-transaction cap/);
});

test("blocks non-allowlisted destinations", () => {
  const plan = planAction({
    action: { ...payment, destination: "wallet:unknown" },
    policy,
  });
  assert.equal(plan.decision, "block");
  assert.match(plan.reason, /allowlisted/);
});

test("blocks payments that exceed the daily cap", () => {
  const ledger = [
    { date: payment.date, amountUsd: 2.8, status: "executed" },
  ];
  const plan = planAction({ action: payment, policy, ledger });
  assert.equal(plan.decision, "block");
  assert.match(plan.reason, /daily spend/);
  assert.equal(spentToday(ledger, payment.date), 2.8);
});

test("refuses execution without named human approval", () => {
  const plan = planAction({ action: payment, policy });
  assert.throws(
    () => executeApproved({ action: payment, plan, approval: null }),
    /Explicit human approval/,
  );
});

test("creates an auditable offline receipt after approval", () => {
  const plan = planAction({ action: payment, policy });
  const result = executeApproved({
    action: payment,
    plan,
    approval: { approved: true, approvedBy: "reviewer-123" },
  });
  assert.equal(result.receipt.status, "executed");
  assert.equal(result.receipt.network, "offline-demo");
  assert.equal(result.receipt.approvedBy, "reviewer-123");
  assert.equal(result.ledger.length, 1);
});
