# Agents / Dev Playbook

## Purpose
Single source of truth for Codex runs, conventions, and QA for the
**Piero Fracasso Perfumes WooCommerce Emails** plugin.

## Project Conventions
- **Plugin slug:** `bypierofracasso-woocommerce-emails`
- **Text domain:** `bypierofracasso-woocommerce-emails`
- **Gateway ID:** `pfp_invoice`
- **Versioning:** bump in main plugin header + README/CHANGELOG on every PR that changes behavior
- **Min requirements:** PHP 7.4+, WooCommerce ≥ 7.x (HPOS-compatible)
- **Languages path:** `/languages` (load on `init`)

## Codex Guidelines
- Keep diffs small, readable; **no binaries**, no minified bundles, don’t touch `vendor/`.
- Prefer incremental PRs (Classic → Blocks → Standards).
- Quote official Woo hooks/APIs explicitly in commands.
- Always include Acceptance Criteria and file “budget”.

## Checkout Integration Checklist
- Classic:
  - Register via `woocommerce_payment_gateways` after Woo: `plugins_loaded` prio 20.
  - `is_available()` = enabled + CHF (+ optional CH/LI + min amount).
  - `$this->supports = ['products']`.
- Blocks:
  - Class extends `AbstractPaymentMethodType`.
  - `get_name() === 'pfp_invoice'`.
  - Register on `woocommerce_blocks_loaded` with IntegrationRegistry (+ legacy filter fallback).
  - JS handle `pfp-invoice-blocks` (deps: `wc-blocks-registry`, `wp-element`, `wp-i18n`).
  - No icons by default.

## Payments Logic
- Settings must provide **QR-IBAN OR IBAN** (one required).
- PDF: QRR if QR-IBAN; SCOR if IBAN + RF; else NON.
- `process_payment()` sets status **`invoice`**.

## Diagnostics
- Log prefix: `[PFP]`.
- Temporary admin-only logs for `is_available()` / `is_active()`.
- WP-CLI: `wp pfp:diag payments` (availability, hooks, script registered).

## Translations
- Use `bypierofracasso-woocommerce-emails` in **all** PHP/JS strings.
- Load domain on `init`.
- JS i18n: `wp_set_script_translations( 'pfp-invoice-blocks', 'bypierofracasso-woocommerce-emails', plugin_dir_path(...) . 'languages' )`.
- POT (optional):
  ```bash
  wp i18n make-pot . languages/bypierofracasso-woocommerce-emails.pot --domain=bypierofracasso-woocommerce-emails
