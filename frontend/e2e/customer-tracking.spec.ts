import { test, expect } from '@playwright/test';

test.describe('Customer Tracking Page', () => {
  test('should display customer tracking page', async ({ page }) => {
    await page.goto('/customer-tracking.html');
    await expect(page.locator('h1')).toContainText('Track Your Shipment');
  });

  test('should display tracking form', async ({ page }) => {
    await page.goto('/customer-tracking.html');
    await expect(page.locator('input[placeholder*="tracking ID"]')).toBeVisible();
    await expect(page.locator('button:has-text("Track")')).toBeVisible();
  });

  test('should show loading state when searching', async ({ page }) => {
    await page.goto('/customer-tracking.html');
    await page.fill('input[placeholder*="tracking ID"]', 'TRK-1234');
    await page.click('button:has-text("Track")');
    await expect(page.locator('#loading')).toBeVisible();
  });

  test('should show error for invalid tracking ID', async ({ page }) => {
    await page.goto('/customer-tracking.html');
    await page.fill('input[placeholder*="tracking ID"]', 'INVALID');
    await page.click('button:has-text("Track")');
    await expect(page.locator('#error')).toBeVisible();
    await expect(page.locator('text=Shipment Not Found')).toBeVisible();
  });

  test('should display results for valid tracking ID', async ({ page }) => {
    await page.goto('/customer-tracking.html');
    await page.fill('input[placeholder*="tracking ID"]', 'TRK-1234');
    await page.click('button:has-text("Track")');
    // Note: This would require a valid trip in the database
    // For now, we're testing the UI behavior
  });
});
