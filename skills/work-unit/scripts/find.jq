# Invocation: jq -n --arg ref VALUE -f find.jq FILE...
if $ref == "" then error("reference must not be empty") else
  [inputs
   | select(
       .id == $ref or .name == $ref
       or (((.emojis // []) | join("")) + " " + .name) == $ref
       or any(.references[]?; .target == $ref)
       or any(.participants[]?; .id == $ref)
       or any(.asana[]?; .task_gid == $ref or .key == $ref or .url == $ref)
       or any(.implementations[]?;
         .repository_url == $ref or .branch == $ref
         or any(.worktree_paths[]?; . == $ref)
         or any(.merge_request_urls[]?; . == $ref)))
   | {file: input_filename, unit: .}]
end
