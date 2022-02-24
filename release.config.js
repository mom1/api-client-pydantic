const { promisify } = require('util')
const readFileAsync = promisify(require('fs').readFile)

const template = readFileAsync('.github/templates/template.hbs')
const commitTemplate = readFileAsync('.github/templates/commit-template.hbs')

const sections = [
  {
    group: 'breaking_changes',
    label: ':boom: Breaking Changes',
    emojis: ['💥'],
  },
  {
    group: 'sparkles',
    label: ':sparkles: New',
    emojis: ['✨', '🎉'],
  },
  {
    group: 'changed',
    label: ':recycle: Changes',
    emojis: ['🎨', '✏️', '⚡️', '♻️', '🔧', '👽️', '🚚', '🍱', '♿️', '💬', '🗃️', '🚸', '🏗️', '📱', '🔥', '🏷️'],
  },
  {
    group: 'fixed',
    label: ':bug: Bugs',
    emojis: ['🐛', '🚑️'],
  },
  {
    group: 'dependencies',
    label: ':arrow_up: Dependencies',
    emojis: ['⬆️', '⬇️', '➕', '➖', '📌'],
  },
  {
    group: 'docs',
    label: ':memo: Documentation',
    emojis: ['📝', '🔇'],
  },
  {
    group: 'other',
    label: ':seedling: Other',
    emojis: ['🔒️', '🔐', '👷', '💄'],
  },
];

function makeGroups(commits) {
  if (!commits.length) return []

  const mapCommits = groups => {
    return groups
      .map(({ group, emojis, label }) => ({
        group,
        label,
        is_dep: group === 'dependencies',
        commits: commits
          .filter((commit) => emojis.indexOf(commit.gitmoji) >= 0)
          .sort((first, second) => new Date(second.committerDate) - new Date(first.committerDate)),
      }))
      .filter(group => group.commits.length)
  }

  return mapCommits(sections)
}
module.exports = {
  branches: ["main", { name: "develop", prerelease: "rc" }],
  tagFormat: "${version}",
  plugins: [
    [
      'semantic-release-gitmoji',
      {
        releaseRules: {
          patch: {
            include: [...sections[2].emojis, ...sections[3].emojis, ...sections[4].emojis, ...sections[5].emojis, ...sections[6].emojis],
            exclude: ['⬆️', '📝'],
          },
        },
        releaseNotes: {
          template,
          partials: { commitTemplate },
          helpers: {
            sections: (commits) => {
              let flat_commits = [];
              for (const [, value] of Object.entries(commits)) {
                flat_commits.push(...value);
              }
              return makeGroups(flat_commits);
            },
            split_by_line: (text) => text.split('\n'),
          },
        }
      }
    ],
    [
      "@semantic-release/changelog",
      {
        changelogFile: "CHANGELOG.md",
        changelogTitle: '# Changelog',
      },
    ],
    [
      "@semantic-release/exec",
      {
        prepareCmd: "poetry version ${nextRelease.version} && poetry build",
        publishCmd: "poetry publish",
      },
    ],
    [
      "@semantic-release/git",
      {
        assets: ["CHANGELOG.md", "pyproject.toml"],
        message: [
          ':bookmark: v${nextRelease.version} [skip ci]',
          '',
          'https://github.com/mom1/api-client-pydantic/releases/tag/${nextRelease.gitTag}'
        ].join('\n')
      },
    ],
    [
      "@semantic-release/github",
      {
        assets: [{ path: "dist/*.whl" }, { path: "dist/*.tar.gz" }],
      },
    ],
  ],
};
