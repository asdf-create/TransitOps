import { test, expect } from '@playwright/test';

test.describe('Vehicles Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/vehicles');
  });

  test('should display vehicles page', async ({ page }) => {
    await expect(page.locator('h2')).toContainText('Vehicles');
  });

  test('should display vehicles table', async ({ page }) => {
    await expect(page.locator('table')).toBeVisible();
    await expect(page.locator('th:has-text("Registration")')).toBeVisible();
    await expect(page.locator('th:has-text("Model")')).toBeVisible();
    await expect(page.locator('th:has-text("Type")')).toBeVisible();
    await expect(page.locator('th:has-text("Status")')).toBeVisible();
  });

  test('should display add vehicle button', async ({ page }) => {
    await expect(page.locator('button:has-text("Add Vehicle")')).toBeVisible();
  });

  test('should navigate back to dashboard', async ({ page }) => {
    await page.click('text=Dashboard');
    await expect(page).toHaveURL('/');
    await expect(page.locator('h2')).toContainText('Dashboard');
  });
});
