from obsidian_to_hugo import ObsidianToHugo

# Paths for your Hugo content and Obsidian vault
hugo_content_dir = "D:/GitLocal/note-repo/content/posts"
obsidian_vault_dir = "D:/GitLocal/blog-md-repo"

obsidian_to_hugo = ObsidianToHugo(
    obsidian_vault_dir=obsidian_vault_dir,
    hugo_content_dir=hugo_content_dir
)

obsidian_to_hugo.run()
