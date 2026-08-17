import { expect, test } from "@playwright/test";

test("home page proves the application runs", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "KDENCE HOUSE Operations" }),
  ).toBeVisible();
  await expect(
    page.getByText("Phase 1 application skeleton is running."),
  ).toBeVisible();
});
