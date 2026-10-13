# API-equivalent model pricing

Usage Overview shows an API-equivalent value separately from actual spend. Expand **API-equivalent model rates** to see each configured model's input, cached-input and output rates per million tokens, its selected-range value and its pricing source

Subscription models use their corresponding standard API catalog entries. Local Gemma 3 4B uses the hosted Gemma 3 4B instruction-tuned entry. Local Qwen 3.5 2B and 4B use the hosted Qwen 3.5 9B entry as an explicitly labeled benchmark. That benchmark is not a published price for the exact local models or a measure of local hardware costs

Rates come from `model_prices_and_context_window.json`. Estimates use the current catalog, including for historical requests, rather than attempting to reconstruct prices on the request date. Long-context tiers are applied to each request, not to the day's combined token count. Cached prompt tokens are discounted when the pricing reference publishes a cache rate; otherwise the normal input rate applies

The report reads existing spend logs using the selected calendar dates and reporting timezone. Successful external requests are included. Failed requests, internal calls and gateway cache hits are excluded. Unknown rates are reported as unavailable and are not counted as free usage. Missing-rate counts indicate a partial estimate

No spend logs, model credentials, budgets or deployment configuration are rewritten. The estimate does not change the amount billed or enforce a hypothetical budget

Proxy admins and read-only admins can request `/model-pricing`, optionally with `start_date`, `end_date` and `timezone_name`. Both model-info endpoints also expose `model_info.api_equivalent_pricing` separately from their existing billing fields
