# What's New in TypeScript 6.0

Apr 15, 2026

TypeScript 6.0 is not a typical feature release. If you upgrade expecting new syntax or dramatic type system changes, you'll be surprised. This release is primarily about modernizing defaults, removing legacy baggage, and preparing the ecosystem for TypeScript 7.0 — the upcoming native port of the compiler and tooling in Go. Understanding what changed and why will save you hours of debugging after upgrading.

## Key Takeaways

- TypeScript 6.0 is a bridge release — the last version built on the JavaScript-based compiler — designed to clean up defaults and deprecations before the native TypeScript 7.0 line arrives.
- Several compiler defaults have changed, including `strict: true`, `module: "esnext"`, a floating `target` that currently resolves to `es2025`, `types: []`, and `noUncheckedSideEffectImports: true`. These can cause build errors if your tsconfig relied on implicit behavior.
- New platform features include the `es2025` target, types for the Temporal API, `RegExp.escape`, `Map.getOrInsert`, and consolidated DOM lib entries.
- Multiple legacy options like `--moduleResolution node` (the old `node10` behavior), `--target es5`, and older module formats are deprecated for the TypeScript 7.0 transition. Address them now to avoid a painful migration later.

## TypeScript 6.0 Is a Bridge Release, Not a Feature Drop

TypeScript 6.0 is intentionally positioned as the last version built on the JavaScript codebase. TypeScript 7.0 is expected to be the native Go-based successor, with much faster builds and editor performance. TypeScript 6.0 cleans up the foundation before that transition happens.

The practical implication: most TypeScript 6.0 changes are about configuration defaults and deprecations, not new language features. If your project has been accumulating legacy tsconfig options, now is the time to address them.

## What's New in TypeScript 6.0: Platform Alignment Features

Despite the transition focus, TypeScript 6.0 does add meaningful support for modern JavaScript APIs.

### ES2025 Target and New Built-in Types

TypeScript 6.0 adds `es2025` as a valid `--target` and `--lib` value. That includes built-in types for APIs like `RegExp.escape`, and also moves some declarations from `esnext` into `es2025`.

It also adds built-in types for newer APIs that are still exposed through `esnext`:

- **`RegExp.escape`** — safely escapes special regex characters in a string
- **`Temporal` API** — a modern replacement for `Date`, typed under `esnext` or `temporal.esnext`
- **`Map.getOrInsert` and `Map.getOrInsertComputed`** — cleaner upsert patterns for `Map` and `WeakMap`, available through `esnext`

```
// Before: verbose Map upsert pattern
if (!map.has("key")) map.set("key", defaultValue)
const value = map.get("key")

// After: clean and concise
const value = map.getOrInsert("key", defaultValue)
```

### DOM Types Consolidation

`dom.iterable` and `dom.asynciterable` are now merged into the base `dom` lib. You no longer need to list them separately in your `tsconfig.json`. If you were using `"lib": ["dom", "dom.iterable"]`, you can simplify to just `"lib": ["dom"]`.

### Subpath Imports Starting with `#/`

TypeScript now supports Node.js subpath imports using the `#/` prefix. That maps cleanly to the `imports` field in `package.json`, and makes the feature feel much closer to the alias patterns bundler users are already familiar with.

## TypeScript 6.0 Breaking Changes: What Will Actually Break Your Project

Several compiler defaults have changed.

| Setting | TypeScript 6.0 Default |
|---|---|
| `strict` | `true` |
| `module` | `esnext` |
| `target` | current supported ES version (`es2025` today) |
| `types` | `[]` (empty) |
| `rootDir` | tsconfig directory |
| `noUncheckedSideEffectImports` | `true` |

The `types: []` change is one of the most impactful. Previously, TypeScript auto-included every package in `node_modules/@types`. Now it includes nothing by default. Projects that rely on globals from `@types/node`, `@types/jest`, or similar packages will see errors like:

```
Cannot find name 'process'. Try adding 'node' to the types field in your tsconfig.
```

Fix it explicitly:

```
{
  "compilerOptions": {
    "types": ["node", "jest"]
  }
}
```

The `rootDir` change is also common. If your output files suddenly appear at `dist/src/index.js` instead of `dist/index.js`, add `"rootDir": "./src"` to your tsconfig.

Another change worth watching is `noUncheckedSideEffectImports: true`. If your codebase has side-effect-only imports with typos or shaky resolution, TypeScript 6.0 is more likely to flag them.

## TypeScript 6.0 Deprecations: What to Remove Before TypeScript 7

These options are deprecated in 6.0 for the TypeScript 7.0 transition, and a few older behaviors are already gone:

- `--target es5` (the lowest supported target is now ES2015)
- `--moduleResolution node` / `--moduleResolution classic` -> migrate to `nodenext` or `bundler`
- `--module amd`, `umd`, `systemjs`, `none`
- `--baseUrl` -> move the prefix into your `paths` entries directly
- `--outFile` -> use a bundler like esbuild, Vite, or Rollup
- `esModuleInterop: false` and `allowSyntheticDefaultImports: false`
- Legacy `module Foo {}` namespace syntax -> use `namespace Foo {}`
- Import `assert` syntax -> replace with `with`

You can silence deprecation warnings temporarily with `"ignoreDeprecations": "6.0"` in your tsconfig, but that should be treated as a short-term stopgap.

## Upgrading to TypeScript 6.0

Install the current 6.0 release candidate with:

```
npm install -D typescript@rc
```

Run `tsc --noEmit` and work through the errors. Most issues will stem from the `types` array, `rootDir`, side-effect imports, and deprecated options.

## Conclusion

TypeScript 6.0 is a cleanup release, not a feature showcase. Its purpose is to retire legacy defaults, align the compiler with modern JavaScript, and prepare the ground for the native TypeScript 7.0 line. The sooner you address these migration changes — updated `types` arrays, explicit `rootDir` values, side-effect import issues, and deprecated option replacements — the smoother your path to TypeScript 7.0 will be.
