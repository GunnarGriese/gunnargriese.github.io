# _plugins/lang_permalink.rb
Jekyll::Hooks.register :posts, :pre_render do |post|
    if post.data['lang'] && post.data['lang'] != 'en'
      post.data['permalink'] = "/#{post.data['lang']}#{post.url}"
    end
  end