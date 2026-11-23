#!/usr/bin/env node
'use strict';

// Installs the authenticity-check skill so `npx @hxp-tools/authenticity-check`
// works. The skill itself is markdown; this only copies files into place.

const fs = require('fs');
const os = require('os');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PKG = require('../package.json');
const NAME = 'authenticity-check';
const SKILL_FILES = ['SKILL.md', 'references'];

const COLORS = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
};

function c(color, text) {
  if (!process.stdout.isTTY || process.env.NO_COLOR) return text;
  return COLORS[color] + text + COLORS.reset;
}

const HOME = os.homedir();
const TARGETS = {
  claude: {
    label: 'Claude Code',
    home: path.join(HOME, '.claude'),
    skills: process.env.CLAUDE_SKILLS_DIR || path.join(HOME, '.claude', 'skills'),
  },
  codex: {
    label: 'Codex',
    home: process.env.CODEX_HOME || path.join(HOME, '.codex'),
    skills: process.env.CODEX_SKILLS_DIR ||
      path.join(process.env.CODEX_HOME || path.join(HOME, '.codex'), 'skills'),
  },
  cursor: {
    label: 'Cursor',
    home: path.join(HOME, '.cursor'),
    skills: process.env.CURSOR_SKILLS_DIR || path.join(HOME, '.cursor', 'skills'),
  },
  windsurf: {
    label: 'Windsurf',
    home: path.join(HOME, '.codeium', 'windsurf'),
    skills: process.env.WINDSURF_SKILLS_DIR ||
      path.join(HOME, '.codeium', 'windsurf', 'skills'),
  },
};

function usage() {
  console.log(`
${c('bold', NAME)} ${c('dim', 'v' + PKG.version)}
Human or machine? Get an honest read.

${c('bold', 'Usage')}
  npx @hxp-tools/authenticity-check@latest              install for detected tools
  npx @hxp-tools/authenticity-check@latest claude codex install for the named tools
  npx @hxp-tools/authenticity-check@latest all          install for every tool below
  npx @hxp-tools/authenticity-check@latest --uninstall  remove what it installed
  npx @hxp-tools/authenticity-check@latest --help

${c('bold', 'Tools')}
${Object.entries(TARGETS)
    .map(([key, t]) => `  ${key.padEnd(9)} ${t.label.padEnd(12)} ${path.join(t.skills, NAME)}`)
    .join('\n')}

  Override a location with CLAUDE_SKILLS_DIR, CODEX_SKILLS_DIR,
  CURSOR_SKILLS_DIR, or WINDSURF_SKILLS_DIR.

${c('bold', 'After install')}
  Restart your coding agent, then ask:
    does this sound like a bot? <paste text>
`);
}

function pickTargets(names) {
  if (names.includes('all')) return Object.keys(TARGETS);
  if (names.length) return names;
  const found = Object.keys(TARGETS).filter((key) => fs.existsSync(TARGETS[key].home));
  return found.length ? found : ['claude'];
}

function isOurs(dest) {
  const skill = path.join(dest, 'SKILL.md');
  if (!fs.existsSync(skill)) return false;
  return /^name: authenticity-check$/m.test(fs.readFileSync(skill, 'utf8'));
}

function install(key) {
  const target = TARGETS[key];
  const dest = path.join(target.skills, NAME);
  if (fs.existsSync(dest) && !isOurs(dest)) {
    console.error(c('red', `  skip ${target.label}: ${dest} exists and is not this skill`));
    return false;
  }
  fs.rmSync(dest, { recursive: true, force: true });
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of SKILL_FILES) {
    fs.cpSync(path.join(ROOT, entry), path.join(dest, entry), { recursive: true });
  }
  console.log(`  ${c('green', 'installed')} ${target.label.padEnd(12)} ${dest}`);
  return true;
}

function uninstall(key) {
  const target = TARGETS[key];
  const dest = path.join(target.skills, NAME);
  if (!fs.existsSync(dest)) return true;
  if (!isOurs(dest)) {
    console.error(c('red', `  skip ${target.label}: ${dest} is not this skill`));
    return false;
  }
  fs.rmSync(dest, { recursive: true, force: true });
  console.log(`  ${c('yellow', 'removed')}   ${target.label.padEnd(12)} ${dest}`);
  return true;
}

function main(argv) {
  const args = argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) {
    usage();
    return 0;
  }
  if (args.includes('--version') || args.includes('-v')) {
    console.log(PKG.version);
    return 0;
  }

  const removing = args.includes('--uninstall');
  const names = args.filter((arg) => !arg.startsWith('-'));
  const unknown = names.filter((name) => name !== 'all' && !TARGETS[name]);
  if (unknown.length) {
    console.error(c('red', `Unknown tool: ${unknown.join(', ')}`));
    usage();
    return 2;
  }

  const keys = removing && !names.length ? Object.keys(TARGETS) : pickTargets(names);
  console.log(`${c('cyan', NAME)} ${c('dim', 'v' + PKG.version)}`);
  const results = keys.map(removing ? uninstall : install);
  if (results.includes(false)) return 1;
  if (!removing) {
    console.log('');
    console.log(c('green', 'Press start: restart your agent, then ask if a text sounds like a bot.'));
    console.log(c('dim', 'Docs: ' + PKG.homepage));
  }
  return 0;
}

process.exitCode = main(process.argv);
