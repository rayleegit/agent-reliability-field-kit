import { executeApproved, planAction } from "./src/policy.mjs";

const policy = {
  perTransactionUsd: 1,
  dailyUsd: 3,
  allowedDestinations: ["marketplace:research-api"],
};

const action = {
  date: "2026-10-23",
  command: "circle services pay --service research-api --amount 0.25",
  destination: "marketplace:research-api",
  amountUsd: 0.25,
};

const plan = planAction({ action, policy });
console.log("Policy decision:");
console.log(JSON.stringify(plan, null, 2));

const result = executeApproved({
  action,
  plan,
  approval: { approved: true, approvedBy: "demo-reviewer" },
});

console.log("\nOffline receipt (no funds moved):");
console.log(JSON.stringify(result.receipt, null, 2));
