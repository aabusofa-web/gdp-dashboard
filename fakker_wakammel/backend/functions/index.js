/**
 * Relays alerts written by a child's device (or a parent's phone during a
 * hand-off) to every parent phone in the family via Firebase Cloud Messaging.
 */
const { onDocumentCreated } = require("firebase-functions/v2/firestore");
const { initializeApp } = require("firebase-admin/app");
const { getFirestore } = require("firebase-admin/firestore");
const { getMessaging } = require("firebase-admin/messaging");

initializeApp();

exports.relayAlert = onDocumentCreated("families/{fid}/alerts/{aid}", async (event) => {
  const alert = event.data?.data();
  if (!alert) return;
  const { fid } = event.params;
  const db = getFirestore();

  const devices = await db.collection(`families/${fid}/devices`).where("role", "==", "parent").get();
  const tokens = devices.docs
    .filter((d) => d.id !== alert.fromDevice && d.data().token)
    .map((d) => d.data().token);
  if (tokens.length === 0) return;

  const important = alert.kind !== "report" && alert.kind !== "levelUp";
  const res = await getMessaging().sendEachForMulticast({
    tokens,
    notification: { title: alert.title || "", body: alert.body || "" },
    data: { kind: String(alert.kind || ""), childId: String(alert.childId || ""), familyId: fid },
    android: {
      priority: important ? "high" : "normal",
      notification: { channelId: important ? "fw_alerts" : "fw_reports" },
    },
  });

  // Forget tokens of uninstalled apps.
  const stale = [];
  res.responses.forEach((r, i) => {
    const code = r.error?.code || "";
    if (code.includes("registration-token-not-registered") || code.includes("invalid-argument")) stale.push(tokens[i]);
  });
  await Promise.all(
    devices.docs.filter((d) => stale.includes(d.data().token)).map((d) => d.ref.update({ token: null }))
  );
});
